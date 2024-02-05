import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedService {

  // Internal assets
  private genresUrl = 'assets/colors.json';

  //Access to our Web API -> Backend 
  //Dev
  // readonly APIUrl = "http://54.219.61.134:8000/";
  //Prod
  readonly APIUrl = "https://ntwrkfy.com/";

  constructor(private http:HttpClient) { }

  // Users 
  signInUser(val:any):Observable<any[]>{
    return this.http.post<any[]>(this.APIUrl + 'api/sign-in', val);
  }

  // logoutUser(val:any):Observable<any[]>{
  //   return this.http.post<any[]>(this.APIUrl + 'api/logout', val);
  // }

  // Spotify API
  getSpotifyAuthSignIn():Observable<any[]>{
    return this.http.get<any[]>(this.APIUrl + 'spotify/get-auth-url');
  } 

  getIsAuthenticated(val:any):Observable<any[]>{
    return this.http.post<any[]>(this.APIUrl + 'spotify/is-authenticated', val);
  } 

  //Genres
  getGenreColor(): Observable<any> {
    return this.http.get(this.genresUrl);
  }

  //Network
  getNetwork(val:any):Observable<any[]>{
    return this.http.post<any[]>(this.APIUrl + 'api/get-network', val);
  }

  // Cross-Functional Concerns
  publish(val:any):Observable<any[]>{
    return this.http.post<any[]>(this.APIUrl + 'cross-functional/publish-message', val);
  }
}
