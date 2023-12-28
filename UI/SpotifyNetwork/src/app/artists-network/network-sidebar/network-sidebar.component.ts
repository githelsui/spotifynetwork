import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';

@Component({
  selector: 'app-network-sidebar',
  templateUrl: './network-sidebar.component.html',
  styleUrl: './network-sidebar.component.css'
})
export class NetworkSidebarComponent {

  @Input() AuthSession:any=null;
  @Input() UserName:string="";
  @Output() TimeFrame = new EventEmitter<string>();
  @Output() AccountSelected = new EventEmitter<boolean>();
  SelectedTimeFrame:string="long_term";
  AllTimeLabel:string=">";
  RecentLabel:string="\u00A0";
  SixMonthsLabel:string="\u00A0";

  setTimeFrame(value:any):void {
    console.log(value)
    var selectedTime = ""
    switch (value) {
      case 1:
        selectedTime = 'long_term';
        this.AllTimeLabel = '>';
        this.RecentLabel = '\u00A0';
        this.SixMonthsLabel = '\u00A0';
        break;
      case 2:
        selectedTime = 'medium_term';
        this.AllTimeLabel = '\u00A0';
        this.RecentLabel = '>';
        this.SixMonthsLabel = '\u00A0';
        break;
      case 3:
        selectedTime = 'short_term';
        this.AllTimeLabel = '\u00A0';
        this.RecentLabel = '\u00A0';
        this.SixMonthsLabel = '>';
        break;
      default:
        selectedTime = 'long_term';
        this.AllTimeLabel = '>';
        this.RecentLabel = '\u00A0';
        this.SixMonthsLabel = '\u00A0';
    }
    this.TimeFrame.emit(selectedTime);
  }

  selectAccount():void {
    this.AccountSelected.emit(true);
  }
}
