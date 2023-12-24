import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-show-network',
  templateUrl: './show-network.component.html',
  styleUrl: './show-network.component.css'
})
export class ShowNetworkComponent implements OnInit {
  @Input() AuthSession:any=null;
  @Input() TimeFrame:string='recent';

  ngOnInit(): void {
    this.setTimeFrame(this.TimeFrame);
  }

  setTimeFrame(data: string) {
    console.log(data)
    this.TimeFrame = data
  }

}
