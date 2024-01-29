import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  API_ROUTE = environment.API_ROUTE;
  BASE_DOMAIN_ROUTE = environment.BASE_DOMAIN_ROUTE;
  private socket!: WebSocket;
  constructor ( private apiService: ApiService){}
  connect(sessionCode: string, usedLanguage: string): Observable<any> {
    const url = `wss://${this.BASE_DOMAIN_ROUTE}/${this.API_ROUTE}/chat_ws/${sessionCode}/ws/${usedLanguage}/${this.apiService.getToken()}`;

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
