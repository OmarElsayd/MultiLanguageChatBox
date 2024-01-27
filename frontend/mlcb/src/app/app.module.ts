import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { LoginComponent } from './login/login.component';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatButtonModule } from '@angular/material/button';
import { HttpClientModule } from '@angular/common/http';
import { HttpClient } from '@angular/common/http';
import { MatToolbarModule } from '@angular/material/toolbar';
import { HomeComponent } from './home/home.component';
import { MatTableModule } from '@angular/material/table';
import { SessionHistroyComponent } from './home/session-histroy/session-histroy.component';
import {MatPaginatorModule} from '@angular/material/paginator';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import { NewSessionComponent } from './home/new-session/new-session.component';
import { MatCheckboxModule } from '@angular/material/checkbox';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatListModule } from '@angular/material/list';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDialogModule } from '@angular/material/dialog';
import { DialogComponent } from './home/dialog/dialog.component';
import { SginupComponent } from './sginup/sginup.component';
import {MatGridListModule} from '@angular/material/grid-list';
import { SpeechService } from './api_services/speech.service';



@NgModule({
  declarations: [
    LoginComponent,
    HomeComponent,
    SessionHistroyComponent,
    NewSessionComponent,
    DialogComponent,
    SginupComponent
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    MatCardModule,
    MatInputModule,
    MatFormFieldModule,
    FormsModule,
    MatButtonModule,
    MatDividerModule,
    MatIconModule,
    MatToolbarModule,
    MatTableModule,
    MatPaginatorModule,
    MatProgressSpinnerModule,
    MatCheckboxModule,
    MatSlideToggleModule,
    MatAutocompleteModule,
    MatListModule,
    MatTabsModule,
    MatDialogModule,
    MatGridListModule
  ],
  providers:[HttpClient, SpeechService],
})

export class AppModule {

  }
  
