import { Component, OnInit } from '@angular/core';
import { SharedService } from '../../shared.service'

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.css'
})
export class SignInComponent implements OnInit {

  //Empty constructor
  constructor(private service:SharedService){}

  //Private variables
  IsAuthenticated:boolean=false;
  LoginLink:string="";

  ngOnInit(): void {
      this.checkIfAuthenticated();
      if(this.IsAuthenticated) {
        console.log("User is authenticated");
      } else {
        console.log("User is NOT authenticated");
      }
  }

  checkIfAuthenticated():void {
    //Api call to DjangoAPI using SharedService
    // console.log("Checking auth - sign-in page")

    // this.service.getIsAuthenticated().subscribe(data=>{
    //   console.log(data)
    //   var isAuth = (data as any).status;
    //   this.IsAuthenticated = isAuth;
    // })
  }

  loginSpotify():void {
    //Api call to DjangoAPI using SharedService
    // response should return a string of the url from the backend
    this.service.getSpotifyAuthSignIn().subscribe(data=>{
      var url = (data as any).url;
      console.log("url: " + url)
      window.location.replace(url)
    })
  }

}
