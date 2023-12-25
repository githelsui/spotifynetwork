import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-network-legend',
  templateUrl: './network-legend.component.html',
  styleUrl: './network-legend.component.css'
})
export class NetworkLegendComponent {

  @Input() TopGenres:any=[];

  //Development Data
  items = [
    { name: 'acoustic', color: '#1f78c1' },
    { name: 'afrobeat', color: '#33a02c' },
    { name: 'alternative', color: '#ff7f00' }
  ];

  selectGenre(genre: any){
    
  }
}
