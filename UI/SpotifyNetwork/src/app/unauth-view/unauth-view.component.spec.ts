import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnauthViewComponent } from './unauth-view.component';

describe('UnauthViewComponent', () => {
  let component: UnauthViewComponent;
  let fixture: ComponentFixture<UnauthViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [UnauthViewComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UnauthViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
