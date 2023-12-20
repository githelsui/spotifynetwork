import { Component } from '@angular/core';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.css'
})
export class SignInComponent {

  public loginSpotify():void {
    console.log("triggerd")
    //Api call to DjangoAPI
  }

}
