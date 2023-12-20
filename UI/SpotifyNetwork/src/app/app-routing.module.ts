import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ArtistsNetworkComponent } from './artists-network/artists-network.component'
import { UserComponent } from './user/user.component'
import { SignInComponent } from './user/sign-in/sign-in.component';

const routes: Routes = [
  {
    path: '', component: SignInComponent
  },
  {
    path: 'artists-network', component: ArtistsNetworkComponent
  },
  {
    path: 'user', component: UserComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
