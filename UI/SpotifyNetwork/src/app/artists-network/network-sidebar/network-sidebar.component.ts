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
  SelectedTimeFrame:string="recent";
  RecentLabel:string=">";
  SixMonthsLabel:string="\u00A0";
  LastYearLabel:string="\u00A0";

  setTimeFrame(value:any):void {
    console.log(value)
    var selectedTime = ""
    switch (value) {
      case 1:
        selectedTime = 'recent';
        this.RecentLabel = '>';
        this.SixMonthsLabel = '\u00A0';
        this.LastYearLabel = '\u00A0';
        break;
      case 2:
        selectedTime = 'last_six_months';
        this.RecentLabel = '\u00A0';
        this.SixMonthsLabel = '>';
        this.LastYearLabel = '\u00A0';
        break;
      case 3:
        selectedTime = 'last_year';
        this.RecentLabel = '\u00A0';
        this.SixMonthsLabel = '\u00A0';
        this.LastYearLabel = '>';
        break;
      default:
        selectedTime = 'recent';
        this.RecentLabel = '>';
        this.SixMonthsLabel = '\u00A0';
        this.LastYearLabel = '\u00A0';
    }
    this.TimeFrame.emit(selectedTime);
  }

  selectAccount():void {
    this.AccountSelected.emit(true);
  }
}
