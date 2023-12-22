import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedService {

  //Access to our Web API -> Backend 
readonly APIUrl = "http://127.0.0.1:8000/";

  constructor(private http:HttpClient) { }

  // Users 
  signInUser(val:any):Observable<any[]>{
    return this.http.post<any[]>(this.APIUrl + 'api/sign-in', val);
  }

  // Spotify API
  getSpotifyAuthSignIn():Observable<any[]>{
    return this.http.get<any[]>(this.APIUrl + 'spotify/get-auth-url');
  } 

  getIsAuthenticated(val:any):Observable<any[]>{
    return this.http.post<any[]>(this.APIUrl + 'spotify/is-authenticated', val);
  } 

  // Artists

  getTopArtists():Observable<any[]>{
    return this.http.get<any[]>(this.APIUrl + '/artists/');
  }

  // Artist Associations

  addArtistAssoc(val:any){
    return this.http.post<any[]>(this.APIUrl + '/artistassocs/', val);
  }  

  getSimilarArtists():Observable<any[]>{
    return this.http.get<any[]>(this.APIUrl + '/artistassocs/');
  }

  getArtistNetwork():Observable<any[]>{
    return this.http.get<any[]>(this.APIUrl + '/artistassocs/');
  }

}
