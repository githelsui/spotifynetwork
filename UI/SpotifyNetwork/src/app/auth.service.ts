import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private cookieKey = 'authorization'; // Change this to your desired cookie key

  constructor(private cookieService: CookieService) {}

  // Save the authorization object in a cookie
  saveAuthorization(authorization: any): void {
    const authorizationJson = JSON.stringify(authorization);
    this.cookieService.set(this.cookieKey, authorizationJson);
  }

  // Get the authorization object from the cookie
  getAuthorization(): any {
    const authorizationJson = this.cookieService.get(this.cookieKey);
    return authorizationJson ? JSON.parse(authorizationJson) : null;
  }

  // Clear the authorization cookie
  clearAuthorization(): void {
    this.cookieService.delete(this.cookieKey);
  }
}
