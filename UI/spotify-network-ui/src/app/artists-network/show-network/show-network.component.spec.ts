import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShowNetworkComponent } from './show-network.component';

describe('ShowNetworkComponent', () => {
  let component: ShowNetworkComponent;
  let fixture: ComponentFixture<ShowNetworkComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ShowNetworkComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ShowNetworkComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
