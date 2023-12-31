import { Component, Input, Output, EventEmitter } from '@angular/core';

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

  logout():void{

  }

  closeModal():void {
    this.CloseModal.emit(false);
  }
}
