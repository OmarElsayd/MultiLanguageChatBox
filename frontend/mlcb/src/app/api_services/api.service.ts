import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private apiUrl = 'http://127.0.0.1:8000/mlcb/api/v1';
  private showSpinnerSubject = new BehaviorSubject<boolean>(false);
  showSpinner$ = this.showSpinnerSubject.asObservable();

  constructor(private http: HttpClient) {}

  getToken(): string | null {
    return localStorage.getItem('Authorization');
  }

  setToken(token: string): void {
    localStorage.setItem('Authorization', token);
  }

  removeToken(): void {
    localStorage.removeItem('Authorization');
  }

  isTokenExpired(): boolean {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.getToken(),
    })
    let curr_user = this.http.get<boolean>(`${this.apiUrl}/verify_access`, { headers } );
    if (curr_user){ return false }
    return true
  }


  login(username: string, password: string): Observable<any> {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    return this.http.post<any>(`${this.apiUrl}/login/`, formData);
  }

  session_history(){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.getToken(),
    });
    return this.http.get<any>(`${this.apiUrl}/session/all`, { headers });
  }

  get_session_histroy(row: any){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.getToken(),
    });
    return this.http.get<any>(`${this.apiUrl}/session/${row.session_code}/history`, { headers })
  }
  
  new_session(invitee: string, passCode: string, is_call: boolean){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.getToken(),
    });
    return this.http.put<any>(`${this.apiUrl}/session/new_session`, {
      "invitee": invitee,
      "passcode": passCode,
      "is_call": is_call
    },
    { headers })
  }

  spinnerShow() {
    this.showSpinnerSubject.next(true);
  }

  spinnerHide() {
    this.showSpinnerSubject.next(false);
  }
}
