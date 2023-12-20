import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ArtistsNetworkComponent } from './artists-network.component';

describe('ArtistsNetworkComponent', () => {
  let component: ArtistsNetworkComponent;
  let fixture: ComponentFixture<ArtistsNetworkComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ArtistsNetworkComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ArtistsNetworkComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
