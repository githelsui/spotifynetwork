import { Component, Input, OnInit, ViewChild, ElementRef, PLATFORM_ID, Inject, HostListener, NgZone } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import * as d3 from 'd3';
import { SharedService } from '../../shared.service'

@Component({
  selector: 'app-show-network',
  templateUrl: './show-network.component.html',
  styleUrl: './show-network.component.css'
})
export class ShowNetworkComponent implements OnInit {
  @ViewChild('graphContainer', { static: true }) graphContainer: ElementRef | undefined;
  @Input() AuthSession:any=null;
  @Input() TimeFrame:string='recent';
  TopGenres:any=[];

  // Private Variables
  Width:number=0;
  Height:number=0;
  GenreColor:any=null;
  GenreLoaded:boolean=false;

  constructor(
    private service:SharedService,
    private zone: NgZone,
    @Inject(PLATFORM_ID) private platformId: Object,
    ){}

  //Development Data
  Nodes:any=[
    { id: 1, name: 'John Lennon', rank: 1, genre: 'acoustic' },
    { id: 2, name: 'Paul McCartney', rank: 2, genre: 'acoustic' },
    { id: 3, name: 'George Harrison', rank: 3, genre: 'acoustic' },
    { id: 4, name: 'Ringo Starr', rank: 4, genre: 'edm' },
    { id: 5, name: 'Bob Dylan', rank: 5, genre: 'edm' },
    { id: 6, name: 'Alice Cooper', rank: 6, genre: 'edm' },
    { id: 7, name: 'Charlie Parker', rank: 7, genre: 'afrobeat' },
    { id: 8, name: 'David Bowie', rank: 8, genre: 'afrobeat' },
    { id: 9, name: 'Eva Cassidy', rank: 9, genre: 'afrobeat' },
    { id: 10, name: 'Frank Sinatra', rank: 10, genre: 'chill' },
    { id: 11, name: 'Grace Jones', rank: 11, genre: 'chill' },
    { id: 12, name: 'Henry Mancini', rank: 12, genre: 'chill' },
    { id: 13, name: 'Ivy Queen', rank: 13, genre: 'blues' },
    { id: 14, name: 'Jack White', rank: 14, genre: 'blues' },
    { id: 15, name: 'Karen Carpenter', rank: 15, genre: 'disco' },
    { id: 16, name: 'Leo Fender', rank: 16, genre: 'disco' },
    { id: 17, name: 'Mia Martini', rank: 17, genre: 'disco' },
    { id: 18, name: 'Nathan East', rank: 18, genre: 'folk' },
    { id: 19, name: 'Olivia Newton-John', rank: 19, genre: 'folk' },
    { id: 20, name: 'Peter Gabriel', rank: 20, genre: 'folk' },
  ];
  Links:any=[  { source: 1, target: 2, weight: 1.5 },
    { source: 2, target: 3, weight: 2.0 },
    { source: 3, target: 4, weight: 1.8 },
    { source: 4, target: 5, weight: 1.2 },
    { source: 5, target: 6, weight: 2.5 },
    { source: 6, target: 7, weight: 1.0 },
    { source: 7, target: 8, weight: 1.7 },
    { source: 8, target: 9, weight: 2.3 },
    { source: 9, target: 10, weight: 1.6 },
    { source: 10, target: 11, weight: 1.9 },
    { source: 11, target: 12, weight: 2.2 },
    { source: 12, target: 13, weight: 1.3 },
    { source: 13, target: 14, weight: 1.1 },
    { source: 14, target: 15, weight: 1.4 },
    { source: 15, target: 16, weight: 1.8 },
    { source: 16, target: 17, weight: 2.1 },
    { source: 17, target: 18, weight: 1.7 },
    { source: 18, target: 19, weight: 2.0 },
    { source: 19, target: 20, weight: 1.5 },];
   
  ngOnInit(): void {
    this.initGraph();
  }

  private setScreenDimensions(): void {
    this.Width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    this.Height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: Event): void {
    this.setScreenDimensions();
  }

  initGraph(): void {
    this.service.getGenreColor().subscribe(
      (data) => {
        this.GenreColor = data;
        this.GenreLoaded = true;
        this.setTimeFrame(this.TimeFrame);
      },
      (error) => {
        console.error('Error loading data:', error);
        this.GenreLoaded = false;
      }
    );
  }

  setTimeFrame(data: string) {
    this.setScreenDimensions();
    this.resetGraph();
    this.TimeFrame = data;
    this.createForceDirectedGraph();
  }

  private resetGraph(): void {
    (this.graphContainer as any).nativeElement.innerHTML =  '';
  }

  private createForceDirectedGraph(): void {
    console.log("width: " + this.Width)
    console.log("height: " + this.Height)
    const svg = d3.select((this.graphContainer as any).nativeElement)
      .append('svg')
      .attr('width', this.Width)
      .attr('height', this.Height)
      .style('cursor', 'pointer');

    const simulation = d3.forceSimulation(this.Nodes as any)
      .force('link', d3.forceLink(this.Links)
        .id((d: any) => d.id)
        .distance((d: any) => this.getLinkDistance(d.weight))) 
      .force('charge', d3.forceManyBody())
      .force('center', d3.forceCenter(this.Width / 2, this.Height / 2));

    const zoom = d3
    .zoom()
    .scaleExtent([1, 10]) // Set the scale extent as needed
    .on('zoom', (event) => zoomed(event));
    svg.call(zoom as any)

    const link = svg.selectAll('line')
      .data(this.Links)
      .enter().append('line')
      .style('stroke', 'black')
      .style('stroke-dasharray', '5,5') 
      .style('cursor', 'pointer')
      .on('mouseover', (event, d) => handleLinkClick(event, d)) 
      .on('mouseout', () => hideTooltip());

    const dragBehavior = d3.drag<SVGGElement, { id: number, name: string }, { id: number, name: string }>()
      .on('start', (event: d3.D3DragEvent<SVGGElement, { id: number, name: string }, { id: number, name: string }>) => dragstarted(event))
      .on('drag', (event: d3.D3DragEvent<SVGGElement, { id: number, name: string }, { id: number, name: string }>) => dragged(event))
      .on('end', (event: d3.D3DragEvent<SVGGElement, { id: number, name: string }, { id: number, name: string }>) => dragended(event));

    const node = svg.selectAll('.node')
    .data(this.Nodes)
    .enter().append('g')
    .attr('class', 'node')
    .append('rect')
    .attr('width', (d: any) => this.getNodeWidth(d.name ,d.rank))  
    .attr('height', (d: any) => this.getNodeHeight(d.rank))
    .attr('dx', 10) // Adjust the position
    .attr('dy', '.5em')
    .attr('fill', (d: any) => this.getNodeColor(d.genre)) 
    .attr('stroke', (d: any) => this.getNodeColor(d.genre)) 
    .attr('stroke-width', 5) // Set the border width
    .style('cursor', 'pointer')
    .on('mouseover', (event, d) => handleNodeClick(event, d)) 
    .on('mouseout', () => hideTooltip())
    .call(dragBehavior as any);

    // Attach text labels to nodes
    const labels = svg.selectAll('.label')
    .data(this.Nodes)
    .enter().append('text')
    .attr('class', 'label')
    .attr('font-size', (d: any) => this.getLabelSize(d.rank))
    .attr('dx', 12) // Adjust the label position
    .attr('dy', '.35em')
    .attr('text-anchor', 'start')
    .attr('dominant-baseline', 'central')
    .attr('fill', 'white')
    .style('cursor', 'pointer')
    .on('mouseover', (event, d) => handleNodeClick(event, d)) 
    .on('mouseout', () => hideTooltip())
    .text((d: any) => (d.name).toUpperCase());

    // create a tooltip
    var tooltip = d3.select((this.graphContainer as any).nativeElement)
    .append("div")
    .attr('height', 50)
    .style("position", "absolute")
    .style("visibility", "hidden")
    .style("background-color", "white")
    .style("border", "solid")
    .style('border', '1px solid gray') 
    .style("padding", "10px");

    simulation
      .on('tick', () => {
        link
          .attr('x1', (d: any) => d.source.x)
          .attr('y1', (d: any) => d.source.y)
          .attr('x2', (d: any) => d.target.x)
          .attr('y2', (d: any) => d.target.y);

        node
          .attr('x', (d: any) => d.x)
          .attr('y', (d: any) => d.y);

        labels
          .attr('x', (d: any) => d.x)
          .attr('y', (d: any) => d.y);
      });

    //hover
    function handleNodeClick(event: any, artist: any) {
      const content = `<div class="d-flex justify-content-center align-items-center">
      <div class="d-flex flex-column">
          <img src='https://github.com/holtzy/D3-graph-gallery/blob/master/img/section/ArcSmal.png?raw=true'>
          <h4>&gt; ${artist.name}</h4>
          <h6>Rank: ${artist.rank}</h6>
          <h6>Genres: ${artist.genre}</h6>
          <h6>Followers: 100</h6>
          <h6>Most Similar: neighbors</h6>
      </div>
      </div>`

      tooltip.html(content);
      tooltip
        .style('left', event.pageX + 10 + 'px')
        .style('top', event.pageY - 10 + 'px')
        .style('visibility', 'visible');
    }

    function handleLinkClick(event: any, link: any) {
      const content = `<div class="d-flex justify-content-center align-items-center">
      <div class="d-flex flex-column">
          <h5>${link.source} and ${link.target}</h5>
          <h5>&gt; Similarity Score: ${link.weight}</h5>
      </div>
      </div>`
      tooltip.html(content);

      // Set tooltip position relative to the mouse pointer
      tooltip
        .style('left', event.pageX + 10 + 'px')
        .style('top', event.pageY - 10 + 'px')
        .style('visibility', 'visible');
    }

    function hideTooltip() {
      tooltip.style('visibility', 'hidden');
    }

    const zone = this.zone;
    function zoomed(event: any) {
      zone.runOutsideAngular(() => {
        requestAnimationFrame(() => {
          svg.attr('transform', event.transform);
        });
      });
    }

    function dragstarted(event: any){
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event: any){
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    function dragended(event: any){
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }
  }

  private getLinkDistance(weight: any): number {
    return 450 * weight;
  }

  // Based on artist.rank
  private getLabelSize(rank: any): number {
    // Lower the rank, the larger the size 
    // const tempRank = -rank;
    const minFontSize = 20;
    const maxFontSize = 60;
    // Transform the rank using a non-linear function
    const transformedRank = 1 / Math.sqrt(Math.abs(rank - 1) + 1);
     // Invert the rank so that lower ranks result in larger font sizes
     // Calculate the font size based on the transformed rank
    const fontSize = minFontSize + (maxFontSize - minFontSize) * transformedRank;

    return Math.min(maxFontSize, Math.max(minFontSize, fontSize));

  }

  //Based on getLabelSize() font size + 2px
  private getNodeHeight(rank: any): number {
    const fontSize = this.getLabelSize(rank);
    return fontSize;
  }

  //Based on width = font size * string length * estimated average width per character 
  private getNodeWidth(label: any, rank: any): number {
    const averageWidthPerCharacter = 0.70;
    const fontSize = this.getLabelSize(rank) as any
    const estimatedWidth =  label.length * fontSize * averageWidthPerCharacter;
    return estimatedWidth;
  }

  private getNodeColor(genre: any){
    if(this.GenreColor != null){
      const color = this.GenreColor.genres[genre]
      console.log(color)
      return color
    } else {
      return "#000000"
    }
  }

  private addTopGenres(data: any){

  }
}
