import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

declare var webkitSpeechRecognition: any;

@Injectable({
  providedIn: 'root'
})
export class SpeechService {

  private recognition: any;
  isStoppedSpeechRecog = false;
  public text = '';
  private voiceToTextSubject: Subject<string> = new Subject();
  private speakingPaused: Subject<any> = new Subject();
  private tempWords: string = '';
  constructor() { 
  }

  speechInput() {
    return this.voiceToTextSubject.asObservable();
  }

  init(lang: string = "en") {
    if (typeof webkitSpeechRecognition !== 'undefined') {
      this.recognition = new webkitSpeechRecognition();
      this.recognition.interimResults = true;
      this.recognition.lang = lang;
      this.setupListeners();

    } else {
      console.error('Speech recognition is not supported in this browser.');
    }
  }

  setupListeners() {
    this.recognition.addEventListener('result', (e: any) => {
      const transcript = Array.from(e.results)
        .map((result: any) => result[0])
        .map((result) => result.transcript)
        .join('');
      this.tempWords = transcript;
      this.voiceToTextSubject.next(this.text || transcript);
    });
    this.recognition.addEventListener('end', (condition: any) => {
      this.recognition.stop();
    });
  }

  startListening(): void {
    if (!this.recognition) {
      throw "error";
    }
    this.isStoppedSpeechRecog = false;
    this.recognition.start();
    console.log(this.recognition);
  }

  stopListening(): void {
    if (!this.recognition) {
      throw "error";
    }
    this.isStoppedSpeechRecog = true;
    this.wordConcat();
    this.recognition.stop();
    this.recognition.isActive = false;
    this.speakingPaused.next('Stopped speaking');
  }

  wordConcat() {
    this.text = this.text.trim() + ' ' + this.tempWords;
    this.text = this.text.trim();
    this.tempWords = '';
  }

  clearText(){
    this.text = "";
  }
}
