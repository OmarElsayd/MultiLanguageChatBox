import { Component, OnDestroy } from '@angular/core';
import { ApiService } from '../../api_services/api.service';
import { Subject, takeUntil } from 'rxjs';
import { WebSocketService } from '../../api_services/web-socket.service';

@Component({
  selector: 'app-new-session',
  templateUrl: './new-session.component.html',
  styleUrl: './new-session.component.scss'
})
export class NewSessionComponent implements OnDestroy{

  constructor(private apiService: ApiService, private webSocketService: WebSocketService){}

  new_session_data_input: boolean = true;
  ask_to_join_contanier: boolean = false;
  start_session_container: boolean = false;

  passCode: string = '';
  userName: string = '';
  isSessionCall: boolean = false;
  session_code: string = '';

  selectedLanguage: string = '';
  availableLanguages: Language[] = [
    { name: 'English', isoCode: 'en' },
    { name: 'Spanish', isoCode: 'es' },
    { name: 'French', isoCode: 'fr' },
    // Add more languages as needed
  ];
  
  private destroy$: Subject<void> = new Subject<void>();

  newSessionSubmit() {
    this.apiService.spinnerShow();
    this.apiService.new_session(this.userName, this.passCode, this.isSessionCall).subscribe(
      (responce) =>{
        if (responce.status_code === 200){
          this.session_code = responce.session_code;
          this.new_session_data_input = false;
          this.ask_to_join_contanier = true;
          this.apiService.spinnerHide();
        }
      }
    )
  }

  join_session(){
    this.apiService.spinnerShow();
    this.ask_to_join_contanier = false;
    this.start_session_container = true;
    this.webSocketService.connect(this.session_code, this.selectedLanguage)
    .pipe(takeUntil(this.destroy$))
    .subscribe(
      (message) => {
        console.log('Received message:', message);
        // Handle received message
      },
      (error) => {
        console.error('WebSocket error:', error);
      },
      () => {
        console.log('WebSocket connection closed.');
      }
    );
    this.apiService.spinnerHide()

  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}

interface Language {
  name: string;
  isoCode: string;
}