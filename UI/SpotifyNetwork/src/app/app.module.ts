import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { UserComponent } from './user/user.component';
import { SignInComponent } from './user/sign-in/sign-in.component';
import { ArtistsNetworkComponent } from './artists-network/artists-network.component';
import { ShowNetworkComponent } from './artists-network/show-network/show-network.component';
import { UnauthViewComponent } from './unauth-view/unauth-view.component';

import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NetworkSidebarComponent } from './artists-network/network-sidebar/network-sidebar.component';
import { NetworkLegendComponent } from './artists-network/show-network/network-legend/network-legend.component';
import { LoadingComponent } from './loading/loading.component';

@NgModule({
  declarations: [
    AppComponent,
    UserComponent,
    SignInComponent,
    ArtistsNetworkComponent,
    ShowNetworkComponent,
    UnauthViewComponent,
    NetworkSidebarComponent,
    NetworkLegendComponent,
    LoadingComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [
    provideClientHydration()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
