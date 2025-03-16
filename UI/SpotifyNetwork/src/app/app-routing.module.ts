import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ArtistsNetworkComponent } from './artists-network/artists-network.component'
import { UserComponent } from './user/user.component'
import { SignInComponent } from './user/sign-in/sign-in.component';
import { UnauthViewComponent } from './unauth-view/unauth-view.component';
import { AboutComponent } from './about/about.component';
import { CreditsComponent } from './credits/credits.component';
import { AudioVisComponent } from './audio-vis/audio-vis.component';

const routes: Routes = [
  {
    path: '', component: SignInComponent
  },
  {
    path: 'artists-network', component: ArtistsNetworkComponent
  },
  {
    path: 'unauth-view', component: UnauthViewComponent
  },
  {
    path: 'about', component: AboutComponent
  },
  {
    path: 'credits', component: CreditsComponent
  },
  {
    path: 'audio-vis', component: AudioVisComponent
  }
   // {
  //   path: 'team', component: TeamComponent
  // }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
