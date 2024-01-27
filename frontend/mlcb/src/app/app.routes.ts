import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { SessionHistroyComponent } from './home/session-histroy/session-histroy.component';
import { NewSessionComponent } from './home/new-session/new-session.component';
import { AuthGuardService, DeActiveAuthGuardService } from './authGuard/auth-guard.service';
import { SginupComponent } from './sginup/sginup.component';

export const routes: Routes = [
    { path: '', redirectTo: '/login', pathMatch: 'full' },
    { path: 'login', component: LoginComponent },
    { path: 'home_page', canActivate: [AuthGuardService], component: HomeComponent},
    { path: "session_histroy", canActivate: [AuthGuardService],canDeactivate: [DeActiveAuthGuardService], component: SessionHistroyComponent } ,
    { path: "new_session", canActivate: [AuthGuardService],canDeactivate: [DeActiveAuthGuardService], component: NewSessionComponent },
    { path: "signup", component: SginupComponent }
];
