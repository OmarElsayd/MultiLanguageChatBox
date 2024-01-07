import { Component } from '@angular/core';
import { ApiService } from '../api_services/api.service';
import { Router } from '@angular/router';



@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  username: string = '';
  password: string = '';

  constructor(private apiService: ApiService, private router: Router) {}

  login() {
    this.apiService.spinnerShow()
    if (this.username && this.password) {
      this.apiService.login(this.username, this.password).subscribe(
        (response) => {
          if (response.status_code == 200){
            localStorage.setItem("Authorization", response.access_token)
            this.apiService.spinnerHide()
            this.router.navigate(['/home_page']);
          }
        },
        (error) => {
          this.apiService.spinnerHide()
          console.error('Login Error:', error);
        }
      );
    }
  }
}
