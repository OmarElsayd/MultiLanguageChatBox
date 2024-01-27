import { AfterViewInit, Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { ApiService } from '../../api_services/api.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { NoteService } from '../../api_services/note.service';
import { BeforeUnloadService } from '../../api_services/before-unload.service';

interface UserData {
  source_lang: string;
  transcript_text: Array<{ text: { before: string; after: string; }; time: string; }>;
}

@Component({
  selector: 'app-session-histroy',
  templateUrl: './session-histroy.component.html',
  styleUrls: ['./session-histroy.component.scss']
})
export class SessionHistroyComponent implements OnInit, AfterViewInit, OnDestroy {
  selectedSession = false;
  user1_ : any = '';
  user2_ : any = '';

  user1Data: any = {};
  user2Data: any = {};
  user1_source_lang = '';
  user2_source_lang = '';
  transcript_text_user1: any[] = [];
  transcript_text_user2: any[] = [];
  dataSourceUser1 = new MatTableDataSource<any>(this.transcript_text_user1);
  dataSourceUser2 = new MatTableDataSource<any>(this.transcript_text_user2);
  sessionList: any[] = [];
  dataSource = new MatTableDataSource<any>(this.sessionList);
  displayedColumns: string[] = ['id', 'created_at', 'end_at', 'participants', 'session_code', 'transcript_id'];
  transcriptDisplayedColumns: string[] = ['textBefore', 'textAfter', 'time'];

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(private apiService: ApiService, private notService: NoteService, private beforeUnloadService: BeforeUnloadService) {}

  ngOnInit() {
    this.loadPage(1, 5);
    this.beforeUnloadService.enableBeforeUnload();
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
  }

  ngOnDestroy() {
    this.beforeUnloadService.disableBeforeUnload();
  }

  loadPage(page: number, pageSize: number) {
    this.apiService.spinnerShow();
    this.apiService.session_history(page, pageSize).subscribe(response => {
    if (response.status_code === 200) {
      if (this.dataSource.paginator){
        this.dataSource.data = response.session_list;
        this.dataSource.paginator.length = response.total_count;
      }
      this.apiService.spinnerHide();
      this.notService.openSnackBar("Sessions Histroy");
      return
    }
    });
    this.apiService.spinnerHide()
    this.notService.openSnackBar("You have no sessions histroy");
  }

  onPageChange(event: PageEvent) {
    this.loadPage(event.pageIndex + 1, event.pageSize);
  }

  getSession(row: any) {
    this.apiService.spinnerShow()
    this.apiService.get_session_histroy(row).subscribe(response => {
      if (response.status_code === 200) {
        this.selectedSession = true;
        this.user1_ = response.transcript.info.user1;
        this.user2_ = response.transcript.info.user2;
        this.processUserData(response.transcript.body, 'user1', this.dataSourceUser1);
        this.processUserData(response.transcript.body, 'user2', this.dataSourceUser2);
        this.apiService.spinnerHide()
        this.notService.openSnackBar(`Session ${row.session_code} is presented`);
      }
    });
  }

  private processUserData(body: any, userKey: 'user1' | 'user2', dataSource: MatTableDataSource<any>) {
    let userData: UserData | undefined;
  
    if (userKey === 'user1') {
      const userIdentifier = this.user1_;
      userData = body[userKey][userIdentifier] as UserData;
    } else if (userKey === 'user2') {
      const userIdentifier = this.user2_;
      userData = body[userKey][userIdentifier] as UserData;
    }
  
    if (userData) {
      if (userKey === 'user1') {
        this.user1Data['source_lang'] = userData.source_lang;
      } else if (userKey === 'user2') {
        this.user2Data['source_lang'] = userData.source_lang;
      }
  
      const transcriptText = userData.transcript_text.map((textItem: { text: { before: string; after: string; }; time: string; }) => ({
        textBefore: textItem.text.before,
        textAfter: textItem.text.after,
        time: textItem.time
      }));
  
      dataSource.data = transcriptText;
    }  
  }
}
