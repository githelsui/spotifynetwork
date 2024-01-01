import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-network-legend',
  templateUrl: './network-legend.component.html',
  styleUrl: './network-legend.component.css'
})
export class NetworkLegendComponent {

  @Input() TopGenres:any=[];
  @Input() ResetGenre:boolean=false;
  @Output() SelectedGenre = new EventEmitter<string>();
  Genre:string="";

  selectGenre(genre: any){
    this.ResetGenre = false;
    this.SelectedGenre.emit(genre)
    this.Genre = genre
  }
  
  getObjectKeys(obj: object): string[] {
    return Object.keys(obj);
  }
}
