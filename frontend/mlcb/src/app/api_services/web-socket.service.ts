import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { API_ROUTE, BASE_DOMAIN_ROUTE } from './const';

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  private socket!: WebSocket;
  constructor ( private apiService: ApiService){}
  connect(sessionCode: string, usedLanguage: string): Observable<any> {
    const url = `wss://${BASE_DOMAIN_ROUTE}/${API_ROUTE}/chat_ws/${sessionCode}/ws/${usedLanguage}/${this.apiService.getToken()}`;

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
