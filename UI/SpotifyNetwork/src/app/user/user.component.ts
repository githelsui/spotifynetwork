import { Component, Input, Output, EventEmitter } from '@angular/core';
import { SharedService } from '../shared.service'
import { AuthService } from '../auth.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrl: './user.component.css'
})
export class UserComponent {
  @Input() AuthSession:any=null;
  @Input() UserName:any="";
  @Input() isVisible = false;
  @Output() CloseModal = new EventEmitter<boolean>();

  constructor(
    private router: Router, 
    private service:SharedService,
    private authService: AuthService
    ){}

  logout():void{
    this.authService.clearAuthorization();
    this.router.navigateByUrl("/", { replaceUrl: true });
  }

  closeModal():void {
    this.CloseModal.emit(false);
  }
}
