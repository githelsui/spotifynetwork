import { Component, OnInit, Output, EventEmitter, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { SharedService } from '../shared.service'
import { AuthService } from '../auth.service';
import { ShowNetworkComponent } from './show-network/show-network.component'

@Component({
  selector: 'app-artists-network',
  templateUrl: './artists-network.component.html',
  styleUrl: './artists-network.component.css'
})
export class ArtistsNetworkComponent implements OnInit{
  
  constructor(
    private router: Router, 
    private route: ActivatedRoute, 
    private service:SharedService,
    private authService: AuthService
    ){}

  //Private variables
  @ViewChild(ShowNetworkComponent, { static: true }) graphView: ShowNetworkComponent | undefined;

  IsAuthenticated:boolean=false;
  MainUrl:string="/artists-network";
  UnauthUrl:string="/unauth-view";
  AuthSession:any=null;
  SelectedTimeFrame:string="long_term";
  AccountSelected:boolean=false;
  UserName:string="";
  
  ngOnInit(): void {
    this.checkIfAuthenticated();
    if(!this.AuthSession){
      this.router.navigateByUrl("/unauth-view", { replaceUrl: true });
    }
  }

  checkIfAuthenticated():void {
    this.AuthSession = this.authService.getAuthorization();
    if(this.AuthSession != null){
      this.UserName = this.AuthSession["UserName"];
    }
  }

  //Receives data from network-sidebar child component
  setTimeFrame(data: string) {
    this.SelectedTimeFrame = data;
    if (this.graphView) {
      this.graphView.setTimeFrame(this.SelectedTimeFrame);
    }
  }

  //Receives data from network-sidebar child component
  setAccountView(data: boolean) {
    this.AccountSelected = data;
    if(this.AccountSelected) {
      this.router.navigateByUrl("/unauth-view", { replaceUrl: true });
    }
  }
}
