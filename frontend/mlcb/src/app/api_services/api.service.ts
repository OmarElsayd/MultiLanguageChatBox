import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { BehaviorSubject, Observable, catchError, map, of } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  API_ROUTE = environment.API_ROUTE;
  BASE_DOMAIN_ROUTE = environment.BASE_DOMAIN_ROUTE;

  private apiUrl = `https://${this.BASE_DOMAIN_ROUTE}/${this.API_ROUTE}`;
  private showSpinnerSubject = new BehaviorSubject<boolean>(false);
  showSpinner$ = this.showSpinnerSubject.asObservable();
  join_session_from_home: boolean = false;

  constructor(private http: HttpClient) {}

  setJoinSession(value: boolean): void {
    this.join_session_from_home = value;
  }
  getToken(): string | null {
    return localStorage.getItem('Authorization');
  }

  setToken(token: string): void {
    localStorage.setItem('Authorization', token);
  }

  removeToken(): void {
    localStorage.removeItem('Authorization');
  }

  isTokenExpired(): Observable<boolean> {
    const token = this.getToken();
    if (!token) {
      return of(true);
    }

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token,
    });

    return this.http.get<boolean>(`${this.apiUrl}/verify_access`, { headers }).pipe(
      map((response: any) => !response),
      catchError(() => of(true))
    );
  }



  login(username: string, password: string): Observable<any> {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    return this.http.post<any>(`${this.apiUrl}/login/`, formData);
  }

  signUp(
    username: string,
    password: string,
    email: string,
    first_name: string,
    last_name: string
  ) {
    const data = {
      user_name: username,
      password: password,
      email: email,
      first_name: first_name,
      last_name: last_name
    };
  
    return this.http.put<any>(`${this.apiUrl}/signup`, data);
  }
  

  confirmEmail(confirmCode: string){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    return this.http.post<any>(`${this.apiUrl}/signup/conf_email?token=${confirmCode}`, {headers});
  }
  
  session_history(page: number = 1, pageSize: number = 5) {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.getToken(),
    });
  
    const params = new HttpParams()
      .set('page', page.toString())
      .set('pagesize', pageSize.toString());
  
    return this.http.get<any>(`${this.apiUrl}/session/all`, { headers, params });
  }
  

  get_session_histroy(row: any){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.getToken(),
    });
    return this.http.get<any>(`${this.apiUrl}/session/${row.session_code}/history`, { headers })
  }
  
  new_session(invitee: string, is_call: boolean){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.getToken(),
    });
    return this.http.put<any>(`${this.apiUrl}/session/new_session`, {
      "invitee": invitee,
      // "passcode": passCode,
      "is_call": is_call
    },
    { headers })
  }

  getUsersInfo(session_code: string){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.getToken(),
    });
    return this.http.get<any>(`${this.apiUrl}/session/${session_code}/info`, 
    { headers })
  }

  spinnerShow() {
    this.showSpinnerSubject.next(true);
  }

  spinnerHide() {
    this.showSpinnerSubject.next(false);
  }
}
