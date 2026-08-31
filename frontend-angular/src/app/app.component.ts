import { Component, computed, effect, inject, signal } from '@angular/core';
import { MatIcon } from '@angular/material/icon';
import { MatMenu, MatMenuItem, MatMenuTrigger } from '@angular/material/menu';
import { MatAnchor, MatButton } from '@angular/material/button';
import { HttpClient } from '@angular/common/http';
import Keycloak, { KeycloakProfile } from 'keycloak-js';
import { MessageResponse } from '@app/models/message-response.model';
import { KEYCLOAK_EVENT_SIGNAL, KeycloakEventType } from 'keycloak-angular';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  imports: [MatIcon, MatMenuTrigger, MatMenu, MatMenuItem, MatButton, MatAnchor]
})
export class AppComponent {

  private readonly httpClient = inject(HttpClient);
  private readonly keycloakEvent = inject(KEYCLOAK_EVENT_SIGNAL);
  protected readonly keycloak = inject(Keycloak);

  protected title = 'angular';
  protected fastApiBase = window.location.origin + "/backend-fastapi/";

  protected readonly apiResponse = signal<string>("");
  protected readonly userProfile = signal<KeycloakProfile | null>(null);
  protected readonly userProfileLoaded = computed(() => this.userProfile() !== null);
  protected readonly isAuthenticated = computed(() => {
    this.keycloakEvent(); // Re-evaluate when a Keycloak event occurs
    return this.keycloak.authenticated;
  });

  constructor() {

    console.log("fastapi base: " + this.fastApiBase);

    effect(() => {
      const event = this.keycloakEvent();
      if (event.type === KeycloakEventType.Ready && this.keycloak.authenticated) {
        this.keycloak.loadUserProfile().then(profile => {
          this.userProfile.set(profile);
        });
      }
      if (event.type === KeycloakEventType.AuthLogout) {
        this.userProfile.set(null);
      }
    });
  }

  protected publicCall() {
    this.httpClient.get<MessageResponse>(this.fastApiBase).subscribe({
      next: res => this.apiResponse.set(res.message),
      error: err => console.error(err)
    });
  }

  protected protectedCall() {
    this.httpClient.get<MessageResponse>(this.fastApiBase + 'my-profile').subscribe({
      next: res => this.apiResponse.set(res.message ),
      error: err => console.error(err)
    });
  }

  protected async login() { await this.keycloak.login(); }

  protected async logout() { await this.keycloak.logout(); }
}
