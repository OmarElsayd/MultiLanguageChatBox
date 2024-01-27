import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class BeforeUnloadService {
  private beforeUnloadListener: (event: BeforeUnloadEvent) => void;

  constructor() {
    this.beforeUnloadListener = (event: BeforeUnloadEvent) => {
      event.preventDefault()
    };
  }

  public enableBeforeUnload(): void {
    window.addEventListener('beforeunload', this.beforeUnloadListener);
  }

  public disableBeforeUnload(): void {
    window.removeEventListener('beforeunload', this.beforeUnloadListener);
  }
}
