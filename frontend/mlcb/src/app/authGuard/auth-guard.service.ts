import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, CanDeactivate, Router, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Observable, map } from 'rxjs';
import { ApiService } from '../api_services/api.service';
import { NoteService } from '../api_services/note.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuardService implements CanActivate {

  constructor(private apiService: ApiService, private router: Router, private noteService: NoteService) { }

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean | UrlTree> | boolean {
    return this.apiService.isTokenExpired().pipe(
      map(isExpired => {
        if (!isExpired) {
          return true;
        } else {
          this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
          this.noteService.openSnackBar("You token is expired. Please login again!")
          localStorage.clear()
          return false;
        }
      })
    );
  }
}

@Injectable({
  providedIn: 'root'
})
export class DeActiveAuthGuardService implements CanDeactivate<any> {
  constructor(private noteService: NoteService) {}

  canDeactivate(): boolean | Observable<boolean> | Promise<boolean> {
    return this.noteService.openDialog("Are you sure you want to leave? Changes you made may not be saved.")
      .pipe(
        map((result) => {
          return result === true;
        })
      );
  }
}