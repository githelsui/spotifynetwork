import { Component, OnInit } from '@angular/core';
import { SharedService } from '../../shared.service'
import { AuthService } from '../../auth.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.css'
})
export class SignInComponent implements OnInit {

  //Empty constructor
  constructor(
    private router: Router, 
    private route: ActivatedRoute, 
    private service:SharedService,
    private authService: AuthService
    ){}

  //Private variables
  IsAuthenticated:boolean=false;
  LoginLink:string="";
  AuthToken:string="";
  AuthSession:any=null;

  ngOnInit(): void {
      this.getSession();
  }

  getSession():void{
    this.route.queryParams.subscribe(params => {
      if('token' in params){
        const token = params['token'];
        if (token) {
          this.AuthToken = token
          this.checkIfAuthenticated();
        } else {
          this.resetAuth()
          this.AuthToken = ''
        }
      }
    });
  }

  checkIfAuthenticated():void {
    if(this.AuthToken != ""){
      var payload = {'session_id': this.AuthToken}
      this.service.getIsAuthenticated(payload).subscribe(data=>{
        this.IsAuthenticated = (data as any).status;
        if(this.IsAuthenticated) { this.loginUser();} 
      })
    } else {// session already exists,  never logged out
      this.sessionExists();
    }
  }

  sessionExists():void{
    this.AuthSession = this.authService.getAuthorization();
    if(this.AuthSession){
      this.router.navigateByUrl("/artists-network", { replaceUrl: true });
    }
  }

   //Button trigger -> authentication page
   loginSpotify():void {
    this.service.getSpotifyAuthSignIn().subscribe(data=>{
      var url = (data as any).url;
      window.location.replace(url)
    })
  }

  loginUser():void{
    var payload = {
      'session_id': this.AuthToken
    }
    this.service.signInUser(payload).subscribe(data=>{
      var user = (data as any).item;
      const authSession = { 
        'SessionId': this.AuthToken,
        'UserEmail': user.UserEmail,
        'UserName': user.UserName
       };
      this.authService.saveAuthorization(authSession);
      this.router.navigateByUrl("/artists-network", { replaceUrl: true });
    },
    error=>{
      console.log("Server Error")
    });
  }

  resetAuth(): void {
    this.authService.clearAuthorization();
  }

  goToBottom(): void{
    window.scrollTo(0,document.body.scrollHeight);
  }

}
