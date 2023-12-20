import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedService {

readonly APIUrl = "http://127.0.0.1:8000/";

  constructor(private http:HttpClient) { }

  // Users 

  addNewUser(val:any){
    return this.http.post<any[]>(this.APIUrl + '/users/', val);
  } 

  getUserInfo(val:any):Observable<any[]>{
    return this.http.get<any[]>(this.APIUrl + '/users/' + val);
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
