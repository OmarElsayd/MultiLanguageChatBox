import { Component, OnDestroy, OnInit } from '@angular/core';
import { NoteService } from '../api_services/note.service';
import { ApiService } from '../api_services/api.service';
import { Router } from '@angular/router';
import { BeforeUnloadService } from '../api_services/before-unload.service';

@Component({
  selector: 'app-sginup',
  templateUrl: './sginup.component.html',
  styleUrl: './sginup.component.scss'
})
export class SginupComponent implements OnInit{
  username: any = '';
  email: any = '';
  password: any = '';
  confirmPassword: any = '';
  firstname: any = '';
  lastname: any = '';
  confirmCode: any = '';
  sginUpForm: boolean = true;
  emailConfirmForm: boolean = false;

  constructor(
    private noteService: NoteService,
    private apiService: ApiService,
    private router: Router,
    private beforeUnloadService: BeforeUnloadService
    ){}
  
  ngOnInit(): void {
      this.beforeUnloadService.enableBeforeUnload()
  }

  signUp(){
    this.apiService.spinnerShow()
    if (!this.username || !this.email || !this.password || !this.confirmPassword){
      this.noteService.openDialog("All fields are required!")
      return
    }

    if (this.password != this.confirmPassword){
      this.noteService.openDialog("Passwords don't match!");
      return
    }

    this.apiService.signUp(
      this.username,
      this.password,
      this.email,
      this.firstname,
      this.lastname
    ).subscribe(
      (response) => {
        if (response.status_code === 200){
          this.sginUpForm = false;
          this.emailConfirmForm = true;
          this.noteService.openSnackBar("Sign up successfully! Please confrim your email");
          this.apiService.spinnerHide()
          return
        }
        this.noteService.openDialog("Unable to sign up. Contact app admin!")
        this.apiService.spinnerHide()
      }
    )
  }

  confirmEmail(){
    this.apiService.spinnerShow()
    if (!this.confirmCode){
      this.noteService.openDialog("Please confrim your email confrimation code")
      return
    }

    this.apiService.confirmEmail(this.confirmCode).subscribe(
      (response) => {
        if (response.status_code === 200){
          this.noteService.openSnackBar("Email was confirmed successfully!")
          this.router.navigate(["/login"]);
          this.apiService.spinnerHide()
          return
        }
        this.noteService.openDialog(
          "Unable to confrim the your email. Please try again or contact app admin"
        )
      }
    )
  }
}
