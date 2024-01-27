import { Component } from '@angular/core';
import { ApiService } from '../api_services/api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  isJoinSession: boolean = false;
  constructor(private apiService: ApiService, private router: Router) {}
  
  sessions_histroy(){
    this.router.navigate(['/session_histroy'])
  }

  new_session(){
    this.router.navigate(['/new_session'])
  }
  joinSession() {
    this.apiService.setJoinSession(true);
    this.router.navigate(["/new_session"])
  }
}
