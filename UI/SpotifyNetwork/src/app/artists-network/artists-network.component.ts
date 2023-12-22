import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { SharedService } from '../shared.service'

@Component({
  selector: 'app-artists-network',
  templateUrl: './artists-network.component.html',
  styleUrl: './artists-network.component.css'
})
export class ArtistsNetworkComponent implements OnInit{

  //Empty constructor
  constructor(private router: Router, private route: ActivatedRoute, private service:SharedService){}

  //Private variables
  IsAuthenticated:boolean=false;
  MainUrl:string="/artists-network";
  UnauthUrl:string="/unauth-view";
  AuthToken:string="";

  // Check if request is authenticated -> if true: access to actual network
  // if false -> redirect to Unauthorized access page
  ngOnInit(): void {
    this.checkIfAuthenticated();
  }

  checkIfAuthenticated():void {
    this.route.queryParams.subscribe(params => {
      const token = params['token'];
      if (token) {
        console.log('token ' + token)
        this.AuthToken = token
      }
    });

    var payload = {
      'session_id': this.AuthToken
    }

    // -- CHECK SPOTIFY AUTH
    console.log("Checking auth - artist-network")
    this.service.getIsAuthenticated(payload).subscribe(data=>{
      this.IsAuthenticated = (data as any).status;
      if(this.IsAuthenticated) {
        // -- SIGN USER INTO WEB APP
        this.router.navigateByUrl(this.MainUrl, { replaceUrl: true });
        console.log("auth access -> render network")
      } else {
        this.router.navigateByUrl(this.UnauthUrl, { replaceUrl: true });
      }
     
    })
 }
}
