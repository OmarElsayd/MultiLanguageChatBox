import { Component, OnDestroy, OnInit } from '@angular/core';
import { ApiService } from '../../api_services/api.service';
import { Subject, takeUntil } from 'rxjs';
import { WebSocketService } from '../../api_services/web-socket.service';
import { NoteService } from '../../api_services/note.service';
import { SpeechService } from '../../api_services/speech.service';

@Component({
  selector: 'app-new-session',
  templateUrl: './new-session.component.html',
  styleUrl: './new-session.component.scss'
})
export class NewSessionComponent implements OnDestroy, OnInit{

  localStorage = localStorage;
  currentUTCTime!: string;
  new_session_data_input: boolean = true;
  ask_to_join_contanier: boolean = false;
  start_session_container: boolean = false;
  join_session_from_home: boolean = false;
  isSessionChatOn: boolean = false;

  passCode: string = '';
  userName: string = '';
  isSessionCall: boolean = false;
  session_code: string = '';
  chatMessages: { sender: any; text: string }[] = [];
  newChatMessage: string = '';
  public isUserSpeaking: boolean = false;

  toUserUserName: string = '';
  toUserUserId!: any;
  selfUserName: string = '';

  selectedLanguage: string = '';
  availableLanguages: Language[] = [
    { name: 'English', isoCode: 'en-US' },
    { name: 'Spanish', isoCode: 'es-ES' },
    { name: 'French', isoCode: 'fr-FR' },
    { name: 'German', isoCode: 'de-DE' },
    { name: 'Chinese', isoCode: 'zh-CN' },
    { name: 'Japanese', isoCode: 'ja-JP' },
    { name: 'Korean', isoCode: 'ko-KR' },
    { name: 'Russian', isoCode: 'ru-RU' },
    { name: 'Arabic', isoCode: 'ar-EG' },
    { name: 'Hindi', isoCode: 'hi-IN' },
    { name: 'Portuguese', isoCode: 'pt-PT' },
    { name: 'Italian', isoCode: 'it-IT' },
    { name: 'Dutch', isoCode: 'nl-NL' },
    { name: 'Swedish', isoCode: 'sv-SE' },
    { name: 'Finnish', isoCode: 'fi-FI' },
    { name: 'Turkish', isoCode: 'tr-TR' },
    { name: 'Polish', isoCode: 'pl-PL' },
    { name: 'Vietnamese', isoCode: 'vi-VN' },
    { name: 'Thai', isoCode: 'th-TH' },
    { name: 'Indonesian', isoCode: 'id-ID' },
    { name: 'Malay', isoCode: 'ms-MY' },
    { name: 'Persian', isoCode: 'fa-IR' },
    { name: 'Hebrew', isoCode: 'he-IL' },
    { name: 'Greek', isoCode: 'el-GR' },
    { name: 'Czech', isoCode: 'cs-CZ' },
    { name: 'Hungarian', isoCode: 'hu-HU' },
    { name: 'Romanian', isoCode: 'ro-RO' },
    { name: 'Danish', isoCode: 'da-DK' },
    { name: 'Norwegian', isoCode: 'no-NO' },
    { name: 'Slovak', isoCode: 'sk-SK' },
    { name: 'Slovenian', isoCode: 'sl-SI' },
    { name: 'Bulgarian', isoCode: 'bg-BG' },
    { name: 'Croatian', isoCode: 'hr-HR' },
    { name: 'Serbian', isoCode: 'sr-RS' },
    { name: 'Estonian', isoCode: 'et-EE' },
    { name: 'Latvian', isoCode: 'lv-LV' },
    { name: 'Lithuanian', isoCode: 'lt-LT' },
];

  
  private destroy$: Subject<void> = new Subject<void>();

  constructor(private speechService: SpeechService, private apiService: ApiService, private webSocketService: WebSocketService, private noteService: NoteService){
    this.join_session_from_home = apiService.join_session_from_home;
  }


  ngOnInit(): void {
    if (this.join_session_from_home){
      this.new_session_data_input = false;
      this.ask_to_join_contanier = true;
    }
  }

  newSessionSubmit() {
    this.apiService.spinnerShow();
    this.apiService.new_session(this.userName, this.passCode, this.isSessionCall).subscribe(
      (responce) =>{
        if (responce.status_code === 200){
          this.session_code = responce.session_code;
          this.new_session_data_input = false;
          this.ask_to_join_contanier = true;
        }
      },
      (error: any) => {
        {
          if (error.status === 404){
            this.noteService.openSnackBar("User is not found.")
          }
          else{
            this.noteService.openSnackBar("Ops! Something went worng. Please contact you admin!")
          }
        }
      }
    );
    this.apiService.spinnerHide();
  }

  join_session(){
    this.apiService.spinnerShow();
    this.ask_to_join_contanier = false;
    this.start_session_container = true;
    this.isSessionChatOn = true;
    this.apiService.getUsersInfo(this.session_code).subscribe(
      (userInfo) =>{
        this.toUserUserName = userInfo.user_name;
        this.toUserUserId = userInfo.id;
        if (userInfo.is_call){
          this.isSessionCall = true;
          // this.speechService.setLanguage(this.selectedLanguage);
          this.speechService.init(this.selectedLanguage);
          this.speechService.speechInput().subscribe((input) => {
            this.newChatMessage = input;
          });
        }
      }
    )
    this.webSocketService.connect(this.session_code, this.selectedLanguage)
    .pipe(takeUntil(this.destroy$))
    .subscribe(
      (message) => {
        console.log('Received message:', message);
        const parsed_message = JSON.parse(message);
        if (parsed_message.status_code === 201){
          this.noteService.openSnackBar(`${parsed_message.user} has joined the chat`);
        }else if (parsed_message.status_code === 410){
          this.noteService.openSnackBar(`${parsed_message.user} has left the chat`);
        }else if (parsed_message.status_code === 423)
        {
          this.noteService.openSnackBar("Session has already ended. navigate to histroy to see the session.", "Center")
          this.start_session_container = false;
          this.ask_to_join_contanier = true;
          this.isSessionChatOn = false;
        }else{
          this.chatMessages.push({ sender: parsed_message.from_, text: parsed_message.content });
        }
      },
      (error) => {
        console.error('WebSocket error:', error);
        this.apiService.spinnerHide()
      },
      () => {
        console.log('WebSocket connection closed.');
        this.webSocketService.close();
      }
    );
    this.apiService.spinnerHide()

  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
    this.ask_to_join_contanier = false;
    this.apiService.setJoinSession(false);
  }

  sendMessage(message: any) {
    const currentDate = new Date();
    let json_message = {
      "type": "message",
      "from_": localStorage.getItem("user_name"),
      "to_": this.toUserUserName,
      "to_user_id": this.toUserUserId,
      "content": message,
      "source_lang": this.selectedLanguage,
      "created_at": currentDate.toUTCString()
    };

    if (this.newChatMessage.trim() !== '') {

      this.webSocketService.send(json_message);

      this.chatMessages.push({ sender: localStorage.getItem("user_name"), text: message });

      this.newChatMessage = '';
    }
  }

  startSpeechToText(): void {
    this.isUserSpeaking = true;
    this.speechService.startListening();
  }

  stopSpeechToText(): void {
    this.speechService.stopListening();
    this.isUserSpeaking = false;
    console.log(this.newChatMessage); 
  }
  

  sendTranscript(): void {
    if (!this.newChatMessage) {
      this.noteService.openSnackBar("No message in the chat to send!");
      return;
    }
    this.sendMessage(this.newChatMessage);
    this.speechService.clearText();
  }
  

}

interface Language {
  name: string;
  isoCode: string;
}