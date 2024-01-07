import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { ApiService } from '../../api_services/api.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';

@Component({
  selector: 'app-session-histroy',
  templateUrl: './session-histroy.component.html',
  styleUrl: './session-histroy.component.scss'
})


export class SessionHistroyComponent implements AfterViewInit{
  sessionList: any[] = [];
  dataSource = new MatTableDataSource<PeriodicElement>(this.sessionList);
  displayedColumns: string[] = ['id', 'created_at', 'end_at', 'participants', 'session_code', 'transcript_id'];

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.apiService.spinnerShow()
    this.apiService.session_history().subscribe((response) => {
      if (response.status_code === 200) {
        this.sessionList = response.session_list;
      }
      this.apiService.spinnerHide()
    });
  }
  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
  }

  getSession(row: any){
    this.apiService.spinnerShow()
    this.apiService.get_session_histroy(row).subscribe((response) => {
      if (response.status_code === 200) {
        let user1_: any = response.transcript.info.user1;
        let user2_: any = response.transcript.info.user2;

        let user1_dict: any = response.transcript.body.user1[user1_]
        let user2_dict: any = response.transcript.body.user2[user2_]

        let user1_source_lang: string = user1_dict["source_lang"]
        let user2_source_lang: string = user2_dict["source_lang"]


        
        console.log("user one dic", user1_dict)
        console.log("user 2 dic", user2_dict)
        
      }
      this.apiService.spinnerHide()
    });
  }
}

export interface PeriodicElement {
  id: string;
  created_at: string;
  end_at: string;
  participants: string;
  session_code: string;
  transcript_id: string;
}