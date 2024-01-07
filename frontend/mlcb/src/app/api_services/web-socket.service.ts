import { HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  private socket!: WebSocket;
  constructor ( private apiService: ApiService){}
  connect(sessionCode: string, usedLanguage: string): Observable<any> {
    const url = `ws://127.0.0.1:8000/mlcb/api/v1/chat_ws/${sessionCode}/ws/${usedLanguage}/${this.apiService.getToken()}`;

    this.socket = new WebSocket(url);

    return new Observable(observer => {
      this.socket.onopen = (event) => {
        console.log('WebSocket opened:', event);
      };

      this.socket.onmessage = (event) => {
        observer.next(event.data);
      };

      this.socket.onclose = (event) => {
        console.log('WebSocket closed:', event);
        observer.complete();
      };

      this.socket.onerror = (event) => {
        console.error('WebSocket error:', event);
        observer.error(event);
      };
    });
  }

  send(message: any): void {
    this.socket.send(JSON.stringify(message));
  }

  close(): void {
    this.socket.close();
  }
}
