import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { SessionHistroyComponent } from './home/session-histroy/session-histroy.component';
import { NewSessionComponent } from './home/new-session/new-session.component';
import { AuthGuardService } from './authGuard/auth-guard.service';

export const routes: Routes = [
    { path: '', redirectTo: '/login', pathMatch: 'full' },
    { path: 'login', component: LoginComponent },
    { path: 'home_page', canActivate: [AuthGuardService], component: HomeComponent},
    { path: "session_histroy", canActivate: [AuthGuardService], component: SessionHistroyComponent } ,
    { path: "new_session", canActivate: [AuthGuardService], component: NewSessionComponent }
];
