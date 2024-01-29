import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarVerticalPosition } from '@angular/material/snack-bar';
import { DialogComponent } from '../home/dialog/dialog.component';

@Injectable({
  providedIn: 'root'
})
export class NoteService {

  constructor(private snackBar: MatSnackBar, private dialog: MatDialog) { }

  openSnackBar(message: string, postion: any = 'bottom', action: string = 'Close', duration: number = 3000) {
    this.snackBar.open(message, action, {
      duration: duration,
      verticalPosition: postion
    });
  }
  openDialog(message: string = "Are you sure you want to do this?") {
    return this.dialog.open(DialogComponent, {
            width: '300px',
            data: { message: message }
        }).afterClosed();
    }
}