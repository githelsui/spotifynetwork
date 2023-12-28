import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ArtistsNetworkComponent } from './artists-network/artists-network.component'
import { UserComponent } from './user/user.component'
import { SignInComponent } from './user/sign-in/sign-in.component';
import { UnauthViewComponent } from './unauth-view/unauth-view.component';
import { LoadingComponent } from './loading/loading.component';

const routes: Routes = [
  {
    path: '', component: SignInComponent
  },
  {
    path: 'artists-network', component: ArtistsNetworkComponent
  },
  {
    path: 'user', component: UserComponent
  },
  {
    path: 'unauth-view', component: UnauthViewComponent
  },
  {
    path: 'dev-only', component: LoadingComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
