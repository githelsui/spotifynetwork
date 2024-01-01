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
  @Input() TimeFrame:string='long_term';
  TopGenres:any=[];

  // Private Variables
  Width:number=0;
  Height:number=0;
  GenreColor:any=null;
  SelectedGenre:any=null;
  Nodes:any=null;
  Links:any=null;
  IsLoading:boolean=true;

  constructor(
    private service:SharedService,
    private zone: NgZone,
    @Inject(PLATFORM_ID) private platformId: Object,
    ){}
   
  ngOnInit(): void {
    //Load network data
    if(this.AuthSession) {
      console.log('timeframe: ' + this.TimeFrame)
      this.loadData();
    }
  }

  private setScreenDimensions(): void {
      this.Width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
      this.Height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;  
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: Event): void {
    this.setScreenDimensions();
  }

  loadData():void {
    this.IsLoading = true;
    var payload = {
      'session_id': this.AuthSession['SessionId'],
      'timeframe': this.TimeFrame
    }
    this.service.getNetwork(payload).subscribe(data=>{
      console.log(data)
      const graph = (data as any).item;
      this.Nodes = (graph as any).Nodes;
      this.Links = (graph as any).Links;
      this.renderContainer();
    })
  }

  renderContainer(): void {
    this.service.getGenreColor().subscribe(
      (data) => {
        this.GenreColor = (data as any).modern_colors;
        this.setUserGenres();
        this.renderGraph();
      },
      (error) => {
        console.error('Error loading data:', error);
      }
    );
  }

  //Preloading data and setting scene for graph rendering
  renderGraph():void {
    this.resetGraph();
    this.setScreenDimensions();
    this.createForceDirectedGraph();
  }

  setTimeFrame(data: any):void {
    this.TimeFrame = data;
    this.resetGraph();
    this.loadData();
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
      .force('charge', d3.forceManyBody().strength(-10))
      .force('collide', d3.forceCollide().radius(150)) // Optional: Force to prevent node overlap
      .force('center', d3.forceCenter(this.Width / 2.5, this.Height / 2.1));

    const zoom = d3
    .zoom()
    .scaleExtent([0.5, 10]) // Set the scale extent as needed
    .on('zoom', (event) => handleZoom(event));
    svg.call(zoom as any)


    const link = svg.selectAll('line')
      .data(this.Links)
      .enter().append('line')
      .style('stroke', 'black')
      .attr("stroke-width", 1.4)
      .style('stroke-dasharray', '7,3') 
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
    .attr('height', 45)
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
      var genres = getGenreList(artist)
      var neighbors = getNeighborList(artist)
      var timeframe = timeframeDetails()
      const content = `<div class="artist-container">
      <div class="d-flex flex-column">
          <img src="${artist.image}" width="300" height="300">
          <h4 style="font-weight: 400; padding-top: 10px">&gt; ${artist.name}</h4>
          <h6 style="font-weight: 400;">/Your #${artist.rank} Most Listened To Artist</h6>
          <h6 style="font-weight: 400;">${timeframe}</h6>
          <h6 style="font-weight: 400;">/Genres:</h6>
          <h6 style="font-weight: 300;">${genres}</h6>
          <h6 style="font-weight: 400;">/Most Similar In Your Network:</h6>
          <h6 style="font-weight: 300;">${neighbors}</h6>
      </div>
      </div>`

      tooltip.html(content);
      tooltip
        .style('left', event.pageX + 10 + 'px')
        .style('top', event.pageY - 10 + 'px')
        .style('visibility', 'visible');
    }

    function handleLinkClick(event: any, link: any) {
      var genres = getGenreList(link)
      const content = `<div class="d-flex justify-content-center align-items-center">
      <div class="d-flex flex-column">
          <h3 style="font-weight: 400;">${link.source_name} and ${link.target_name}</h3>
          <h5 style="font-weight: 300;">&gt; Similarity Score: ${link.weight}</h5>
          <h6 style="font-weight: 300;">Similarity based on the likelihood<br> of ${link.source_name}'s audience listening to ${link.target_name}</h6>
          <br>
          <h5 style="font-weight: 300;">&gt; Shared Genres: ${genres}</h5>
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

    const timeframe = this.TimeFrame;
    function timeframeDetails(){
      if(timeframe == "long_term"){
        return "since your account creation"
      }
      if(timeframe == "medium_term"){
        return "in the last 6 months"
      }
      if(timeframe == "short_term"){
        return "in the last 4 weeks"
      }
      return ""
    }

    function getGenreList(data: any){
      return data.genres.map((genres: any, index: any) => {
        // Add a line break after every two strings, except for the first string
        const separator = index % 2 === 1 && index !== 0 ? '<br>' : '';
    
        // Add a comma if it's not the last string
        const comma = index < data.genres.length - 1 ? ', ' : '';
    
        return genres + comma + separator;
      }).join('');
    }

    function getNeighborList(data: any){
      return data.neighbors.map((neighbors: any, index: any) => {
        // Add a line break after every two strings, except for the first string
        const separator = index % 2 === 1 && index !== 0 ? '<br>' : '';
    
        // Add a comma if it's not the last string
        const comma = index < data.neighbors.length - 1 ? ', ' : '';
    
        return neighbors + comma + separator;
      }).join('');
    }

    function handleZoom(event: any) {
      // Update the positions of nodes based on the zoom transformation
      node.attr("transform", event.transform);
      link.attr("transform", event.transform);
      labels.attr("transform", event.transform);
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

    this.IsLoading = false;
  }

  private getLinkDistance(weight: any): number {
    // const avgDistance = (this.Width + this.Height) / 2;
    const maxLinkDistance = Math.min(this.Width, this.Height);
    const minNodeWeight = 1;
    const maxNodeWeight = 20;
    // Normalize node weight between 0 and 1
    const normalizedWeight = (weight) / (maxNodeWeight - minNodeWeight);
    // Calculate link distance based on normalized weight
    const linkDistance = (normalizedWeight * 0.85) * (maxLinkDistance);
    // return (this.Height / weight);
    return linkDistance;
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
    if(this.TopGenres != null){
      const color = this.TopGenres[genre]
      return color
    } else {
      return "#000000"
    }
  }

  private setUserGenres(){
    let genreSet = new Set(); // Does not accept duplicate genres
    let topGenres = {}
    for(let artist of this.Nodes){
      // Create a genre dict with genre: color_code
      genreSet.add(artist.genre)
    }
    var i = 0;
    for(let genre of genreSet as any){
      (topGenres as any)[genre]= this.GenreColor[i]
      i++;
    }
    this.TopGenres = topGenres
  }

  // Receives data from legend selection child component
  setSelectedGenre(genre: string) {
    this.SelectedGenre = genre;
  }
}
