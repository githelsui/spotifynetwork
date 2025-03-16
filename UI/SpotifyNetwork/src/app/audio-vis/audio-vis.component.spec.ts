import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AudioVisComponent } from './audio-vis.component';

describe('AudioVisComponent', () => {
  let component: AudioVisComponent;
  let fixture: ComponentFixture<AudioVisComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AudioVisComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AudioVisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
