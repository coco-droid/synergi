const customNodes = {
    component: [
      {
        name: "navigateur-web",
        icon: "<i class='fas fa-globe'></i><span> Navigateur Web</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-globe'></i> Navigateur Web</div>
            <div class="box">
              <p>Action de navigation</p>
              <input type="text" df-url placeholder="URL">
              <input type="text" df-form-data placeholder="Données du formulaire">
              <input type="text" df-screenshot-path placeholder="Chemin de capture d'écran">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          url: "",
          formData: "",
          screenshotPath: "",
        },
      },
      {
        name: "commandes-systeme",
        icon: "<i class='fas fa-terminal'></i><span> Commandes Système</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-terminal'></i> Commandes Système</div>
            <div class="box">
              <p>Commande système</p>
              <input type="text" df-command placeholder="Commande système">
            </div>
          </div>
        `,
        input: 1,
        output: 1,
        params: {
          command: "",
        },
      },
      {
        name: "generation-documents",
        icon: "<i class='far fa-file-alt'></i><span> Génération de Documents</span>",
        html: `
          <div>
            <div class="title-box"><i class='far fa-file-alt'></i> Génération de Documents</div>
            <div class="box">
              <p>Type de document</p>
              <input type="text" df-document-type placeholder="Type de document">
              <input type="text" df-document-data placeholder="Données du document">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          documentType: "",
          documentData: "",
        },
      },
      {
        name: "automatisation-projet",
        icon: "<i class='fas fa-tasks'></i><span> Automatisation de la Gestion de Projet</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-tasks'></i> Automatisation de la Gestion de Projet</div>
            <div class="box">
              <p>Tâche</p>
              <input type="text" df-task placeholder="Nom de la tâche">
              <input type="text" df-deadline placeholder="Date limite">
              <input type="text" df-resources placeholder="Ressources">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          task: "",
          deadline: "",
          resources: "",
        },
      },
      {
        name: "envoi-courriels",
        icon: "<i class='far fa-envelope'></i><span> Envoi de Courriels</span>",
        html: `
          <div>
            <div class="title-box"><i class='far fa-envelope'></i> Envoi de Courriels</div>
            <div class="box">
              <p>Destinataire</p>
              <input type="text" df-recipient placeholder="Adresse e-mail du destinataire">
              <input type="text" df-subject placeholder="Objet du courriel">
              <input type="text" df-message placeholder="Corps du courriel">
              <input type="text" df-attachment placeholder="Pièce jointe">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          recipient: "",
          subject: "",
          message: "",
          attachment: "",
        },
      },
      {
        name: "generation-code",
        icon: "<i class='fas fa-code'></i><span> Génération de Code</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-code'></i> Génération de Code</div>
            <div class="box">
              <p>Langage de programmation</p>
              <input type="text" df-programming-language placeholder="Langage de programmation">
              <input type="text" df-code-specification placeholder="Spécification du code">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          programmingLanguage: "",
          codeSpecification: "",
        },
      },
      {
        name: "extraction-donnees-web",
        icon: "<i class='fas fa-database'></i><span> Extraction de Données Web</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-database'></i> Extraction de Données Web</div>
            <div class="box">
              <p>Site web</p>
              <input type="text" df-website placeholder="URL du site web">
              <input type="text" df-data-placeholder="Données extraites">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          website: "",
          data: "",
        },
      },
      {
        name: "manipulation-fichiers",
        icon: "<i class='fas fa-file'></i><span> Manipulation de Fichiers</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-file'></i> Manipulation de Fichiers</div>
            <div class="box">
              <p>Action sur les fichiers</p>
              <input type="text" df-file-action placeholder="Action sur les fichiers">
              <input type="text" df-file-path placeholder="Chemin du fichier">
              <input type="text" df-destination-path placeholder="Chemin de destination">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          fileAction: "",
          filePath: "",
          destinationPath: "",
        },
      },
      {
        name: "conversion-fichiers",
        icon: "<i class='fas fa-file-contract'></i><span> Conversion de Fichiers</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-file-contract'></i> Conversion de Fichiers</div>
            <div class="box">
              <p>Type de conversion</p>
              <input type="text" df-conversion-type placeholder="Type de conversion">
              <input type="text" df-source-file placeholder="Fichier source">
              <input type="text" df-destination-file placeholder="Fichier de destination">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          conversionType: "",
          sourceFile: "",
          destinationFile: "",
        },
      },
      {
        name: "planification-taches",
        icon: "<i class='fas fa-calendar'></i><span> Planification de Tâches</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-calendar'></i> Planification de Tâches</div>
            <div class="box">
              <p>Planification</p>
              <input type="text" df-task-name placeholder="Nom de la tâche">
              <input type="text" df-task-deadline placeholder="Date limite de la tâche">
              <input type="text" df-task-recurrence placeholder="Récurrence de la tâche">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          taskName: "",
          taskDeadline: "",
          taskRecurrence: "",
        },
      },
      {
        name: "gestion-base-donnees",
        icon: "<i class='fas fa-database'></i><span> Gestion de Base de Données</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-database'></i> Gestion de Base de Données</div>
            <div class="box">
              <p>Action sur la base de données</p>
              <input type="text" df-database-action placeholder="Action sur la base de données">
              <input type="text" df-database-query placeholder="Requête SQL">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          databaseAction: "",
          databaseQuery: "",
        },
      },
      {
        name: "traitement-images",
        icon: "<i class='fas fa-image'></i><span> Traitement d'Images</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-image'></i> Traitement d'Images</div>
            <div class="box">
              <p>Action de traitement d'image</p>
              <input type="text" df-image-action placeholder="Action de traitement d'image">
              <input type="text" df-image-path placeholder="Chemin de l'image">
              <input type="text" df-image-output-path placeholder="Chemin de sortie de l'image">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          imageAction: "",
          imagePath: "",
          imageOutputPath: "",
        },
      },
      {
        name: "reconnaissance-texte",
        icon: "<i class='fas fa-font'></i><span> Reconnaissance de Texte</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-font'></i> Reconnaissance de Texte</div>
            <div class="box">
              <p>Image ou PDF</p>
              <input type="text" df-image-pdf placeholder="Chemin de l'image ou du PDF">
              <input type="text" df-text-output placeholder="Texte extrait">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          imagePdf: "",
          textOutput: "",
        },
      },
      {
        name: "automatisation-medias-sociaux",
        icon: "<i class='fab fa-twitter'></i><span> Automatisation des Médias Sociaux</span>",
        html: `
          <div>
            <div class="title-box"><i class='fab fa-twitter'></i> Automatisation des Médias Sociaux</div>
            <div class="box">
              <p>Plate-forme de médias sociaux</p>
              <input type="text" df-social-platform placeholder="Plate-forme de médias sociaux">
              <input type="text" df-social-message placeholder="Message à publier">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          socialPlatform: "",
          socialMessage: "",
        },
      },
      {
        name: "gestion-fichiers-cloud",
        icon: "<i class='fas fa-cloud'></i><span> Gestion de Fichiers Cloud</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-cloud'></i> Gestion de Fichiers Cloud</div>
            <div class="box">
              <p>Service de stockage cloud</p>
              <input type="text" df-cloud-service placeholder="Service de stockage cloud">
              <input type="text" df-cloud-action placeholder="Action sur les fichiers">
              <input type="text" df-cloud-file placeholder="Fichier à manipuler">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          cloudService: "",
          cloudAction: "",
          cloudFile: "",
        },
      },
      {
        name: "analyse-donnees",
        icon: "<i class='fas fa-chart-bar'></i><span> Analyse de Données</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-chart-bar'></i> Analyse de Données</div>
            <div class="box">
              <p>Données à analyser</p>
              <input type="text" df-data-analysis placeholder="Données à analyser">
              <input type="text" df-analysis-type placeholder="Type d'analyse">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          dataAnalysis: "",
          analysisType: "",
        },
      },
      {
        name: "automatisation-rapports",
        icon: "<i class='far fa-file-alt'></i><span> Automatisation des Rapports</span>",
        html: `
          <div>
            <div class="title-box"><i class='far fa-file-alt'></i> Automatisation des Rapports</div>
            <div class="box">
              <p>Données pour le rapport</p>
              <input type="text" df-report-data placeholder="Données pour le rapport">
              <input type="text" df-report-template placeholder="Modèle de rapport">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          reportData: "",
          reportTemplate: "",
        },
      },
      {
        name: "api-externes",
        icon: "<i class='fas fa-external-link-alt'></i><span> Interactions avec des API Externes</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-external-link-alt'></i> Interactions avec des API Externes</div>
            <div class="box">
              <p>API externe</p>
              <input type="text" df-external-api placeholder="API externe">
              <input type="text" df-api-action placeholder="Action API">
              <input type="text" df-api-data placeholder="Données API">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          externalApi: "",
          apiAction: "",
          apiData: "",
        },
      },
      {
        name: "conversation-chatbots",
        icon: "<i class='far fa-comment-alt'></i><span> Scénarios de Conversation (Chatbots)</span>",
        html: `
          <div>
            <div class="title-box"><i class='far fa-comment-alt'></i> Scénarios de Conversation (Chatbots)</div>
            <div class="box">
              <p>Scénario de conversation</p>
              <input type="text" df-chatbot-scenario placeholder="Scénario de conversation">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          chatbotScenario: "",
        },
      },
      {
        name: "automatisation-reunions",
        icon: "<i class='far fa-calendar-alt'></i><span> Automatisation des Réunions</span>",
        html: `
          <div>
            <div class="title-box"><i class='far fa-calendar-alt'></i> Automatisation des Réunions</div>
            <div class="box">
              <p>Détails de la réunion</p>
              <input type="text" df-meeting-details placeholder="Détails de la réunion">
              <input type="text" df-participants placeholder="Participants">
              <input type="text" df-meeting-date placeholder="Date de la réunion">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          meetingDetails: "",
          participants: "",
          meetingDate: "",
        },
      },
      {
        name: "generation-contenu",
        icon: "<i class='fas fa-file-alt'></i><span> Génération de Contenu</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-file-alt'></i> Génération de Contenu</div>
            <div class="box">
              <p>Type de contenu</p>
              <input type="text" df-content-type placeholder="Type de contenu">
              <input type="text" df-content-data placeholder="Données du contenu">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          contentType: "",
          contentData: "",
        },
      },
      {
        name: "gestion-taches-administratives",
        icon: "<i class='fas fa-tasks'></i><span> Gestion des Tâches Administratives</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-tasks'></i> Gestion des Tâches Administratives</div>
            <div class="box">
              <p>Tâche administrative</p>
              <input type="text" df-admin-task placeholder="Tâche administrative">
              <input type="text" df-admin-details placeholder="Détails de la tâche">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          adminTask: "",
          adminDetails: "",
        },
      },
      {
        name: "controle-eclairage-appareils",
        icon: "<i class='fas fa-lightbulb'></i><span> Contrôle de l'Éclairage et des Appareils</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-lightbulb'></i> Contrôle de l'Éclairage et des Appareils</div>
            <div class="box">
              <p>Action de contrôle</p>
              <input type="text" df-control-action placeholder="Action de contrôle">
              <input type="text" df-device-name placeholder="Nom de l'appareil">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          controlAction: "",
          deviceName: "",
        },
      },
      {
        name: "analyse-sentiment",
        icon: "<i class='far fa-smile'></i><span> Analyse de Sentiment</span>",
        html: `
          <div>
            <div class="title-box"><i class='far fa-smile'></i> Analyse de Sentiment</div>
            <div class="box">
              <p>Commentaires ou avis</p>
              <input type="text" df-sentiment-input placeholder="Commentaires ou avis">
              <input type="text" df-sentiment-result placeholder="Résultat de l'analyse">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          sentimentInput: "",
          sentimentResult: "",
        },
      },
      {
        name: "automatisation-recherche",
        icon: "<i class='fas fa-search'></i><span> Automatisation de la Recherche</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-search'></i> Automatisation de la Recherche</div>
            <div class="box">
              <p>Mots-clés de recherche</p>
              <input type="text" df-search-keywords placeholder="Mots-clés de recherche">
              <input type="text" df-search-results placeholder="Résultats de la recherche">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          searchKeywords: "",
          searchResults: "",
        },
      },
      {
        name: "traduction-texte",
        icon: "<i class='fas fa-language'></i><span> Traduction de Texte</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-language'></i> Traduction de Texte</div>
            <div class="box">
              <p>Texte à traduire</p>
              <input type="text" df-text-translate placeholder="Texte à traduire">
              <input type="text" df-translation-result placeholder="Résultat de la traduction">
              <input type="text" df-target-language placeholder="Langue cible">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          textTranslate: "",
          translationResult: "",
          targetLanguage: "",
        },
      },
      {
        name: "controle-musique",
        icon: "<i class='fas fa-music'></i><span> Contrôle de la Musique</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-music'></i> Contrôle de la Musique</div>
            <div class="box">
              <p>Action de contrôle musical</p>
              <input type="text" df-music-control-action placeholder="Action de contrôle musical">
              <input type="text" df-music-platform placeholder="Plateforme musicale">
              <input type="text" df-music-track placeholder="Titre de la musique">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          musicControlAction: "",
          musicPlatform: "",
          musicTrack: "",
        },
      },
      {
        name: "analyse-donnees-financieres",
        icon: "<i class='fas fa-chart-line'></i><span> Analyse de Données Financières</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-chart-line'></i> Analyse de Données Financières</div>
            <div class="box">
              <p>Données financières</p>
              <input type="text" df-financial-data placeholder="Données financières">
              <input type="text" df-financial-analysis placeholder="Type d'analyse financière">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          financialData: "",
          financialAnalysis: "",
        },
      },
      {
        name: "gestion-notifications",
        icon: "<i class='far fa-bell'></i><span> Gestion des Notifications</span>",
        html: `
          <div>
            <div class="title-box"><i class='far fa-bell'></i> Gestion des Notifications</div>
            <div class="box">
              <p>Notification</p>
              <input type="text" df-notification-text placeholder="Texte de la notification">
              <input type="text" df-notification-trigger placeholder="Déclencheur de la notification">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          notificationText: "",
          notificationTrigger: "",
        },
      },
      {
        name: "automatisation-tests",
        icon: "<i class='fas fa-vial'></i><span> Automatisation des Tests</span>",
        html: `
          <div>
            <div class="title-box"><i class='fas fa-vial'></i> Automatisation des Tests</div>
            <div class="box">
              <p>Scénario de test</p>
              <input type="text" df-test-scenario placeholder="Scénario de test">
            </div>
          </div>
        `,
        input: 0,
        output: 1,
        params: {
          testScenario: "",
        },
      },
      // Ajoutez d'autres nœuds personnalisés ici
    ],
  };
  