import { Component, ViewChild, ElementRef } from '@angular/core';

@Component({
  selector: 'app-audio-vis',
  templateUrl: './audio-vis.component.html',
  styleUrl: './audio-vis.component.css'
})
export class AudioVisComponent {
  @ViewChild('visualizer')
  private visualizerRef: ElementRef = {} as ElementRef;

  context = new AudioContext();
  analyserNode = new AnalyserNode(this.context, { fftSize: 256 });
  gainNode = new GainNode(this.context, { gain: 0.6 });
  bassEQ = new BiquadFilterNode(this.context, {
    type: 'lowshelf',
    frequency: 500,
    gain: 10
  });
  midEQ = new BiquadFilterNode(this.context, {
    type: 'peaking',
    Q: Math.SQRT1_2,
    frequency: 100,
    gain: 5
  });
  trebleEQ = new BiquadFilterNode(this.context, {
    type: 'highshelf',
    frequency: 100,
    gain: 10
  });

  constructor() { }

  ngOnInit(): void {
    this.setupContext();
    this.resize();
    this.drawVisualizer();
    window.addEventListener('resize', this.resize.bind(this)); // Handle resize events
  }

  ngOnDestroy(): void {
    this.context.close(); // Clean up when component is destroyed
    // window.removeEventListener('resize', this.resize.bind(this)); // Remove resize event listener
  }

  async setupContext(): Promise<void> {
    const guitar = await this.getGuitar();
    if (this.context.state === 'suspended') {
      await this.context.resume();
    }
    const source = this.context.createMediaStreamSource(guitar);
    source
      .connect(this.bassEQ)
      .connect(this.midEQ)
      .connect(this.trebleEQ)
      .connect(this.gainNode)
      .connect(this.analyserNode)
      .connect(this.context.destination);
  }

  getGuitar(): Promise<MediaStream> {
    return navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: false,
        autoGainControl: false,
        noiseSuppression: false
      }
    });
  }

  drawVisualizer(): void {
    requestAnimationFrame(this.drawVisualizer.bind(this));

    const visualizer = this.visualizerRef.nativeElement;
    const bufferLength = this.analyserNode.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    this.analyserNode.getByteFrequencyData(dataArray);
    const width = visualizer.width;
    const height = visualizer.height;
    const barWidth = (width / bufferLength) * 5;

    const canvasContext = visualizer.getContext('2d');
    canvasContext.clearRect(0, 0, width, height);

    dataArray.forEach((item, index) => {
      const dataLabel = (item / 255 * height / 2).toPrecision(9);
      const y = (item / 255 * height / 2) * 2.3;
      const x = barWidth * index;

      canvasContext.fillStyle = `hsl(0, 100%, 99%)`;
      canvasContext.strokeStyle = 'black';
      canvasContext.strokeRect(x, height - y, 1, y);
      canvasContext.fillRect(x, height - y, 1, y);

      // Data text labels
      canvasContext.font = "20px monospace";
      canvasContext.lineWidth = 1;
      canvasContext.fillStyle = '#000';
      canvasContext.fillText(dataLabel, x, height - y);
    });
  }

  resize(): void {
    const visualizer = this.visualizerRef.nativeElement;
    visualizer.width = visualizer.clientWidth * window.devicePixelRatio;
    visualizer.height = visualizer.clientWidth * window.devicePixelRatio;
  }
}
