# Migration Plan: Image Backup Tool - Python zu C# WPF

**Erstellt am:** 2026-06-29  
**Ziel:** Migration des Python-basierten `backup_images.py` Skripts zu einer modernen, wartbaren und erweiterbaren C# WPF Anwendung

---

## 1. Analyse des bestehenden Python-Skripts

### 1.1 Hauptfunktionalitäten

Das Python-Skript bietet folgende Kernfunktionen:

#### A. Backup-Operationen
- **Backup images**: Erstellt Backups von PNG- und WEBM-Dateien aus `game/images` in zwei separate Backup-Ordner
  - Ziel 1: `Mind the School Image Backup`
  - Ziel 2: `Mind the School Full Image Backup`
  - Verwendet `shutil.copy2()` zur Erhaltung von Metadaten

#### B. Extract-Operationen
- **Extract new images**: Verschiebt PNG-Dateien in den Extract-Ordner
  - Optional: Purge des Extract-Ordners vor der Operation
  - Verwendet `shutil.move()` für das Verschieben
- **Copy new images to Extract**: Kopiert PNG-Dateien in den Extract-Ordner (ohne zu verschieben)

#### C. Konvertierungs-Operationen
- **Convert images**: Konvertiert PNG zu WEBP mit NConvert.exe
  - Lossless-Modus: `-q -1` für alle Dateien
  - Lossy-Modus: `-q 90` nur für bestimmte Verzeichnisse (events, background, characters, mods)
  - Andere Verzeichnisse werden immer lossless konvertiert
  - Batch-Verarbeitung mit Fortschrittsausgabe in Konsole

#### D. Return-Operationen
- **Return modified images**: Kopiert konvertierte WEBP-Dateien zurück nach `game/images`
- **Return Videos**: Kopiert WEBM-Dateien zurück nach `game/images`

#### E. Versionierte Backups
- **Move Images to Versioned Backup**: 
  - Auswahl des Zielordners aus vorhandenen Versionen
  - Auswahl zwischen lossy/lossless Unterordner
  - Unterstützt PNG, WEBM und WEBP
- **Return Images from Versioned Backup**:
  - Modi: "All" oder "Only existing" (überschreibt nur existierende Dateien)
  - Auswahl der Quellversion und lossy/lossless Variante

#### F. Utility-Operationen
- **Clean Extract**: Löscht alle Unterordner im Extract-Verzeichnis
- **Move Backup to Extract**: Verschiebt PNG-Dateien von Backup zu Extract
- **Count**: Zählt Bilder und Videos in verschiedenen Verzeichnissen (Game, Extract, Backup, Versioned)
- **Compare images**: Vergleicht Dateien zwischen Verzeichnissen und zeigt fehlende Gegenstücke
  - Modi: game → backup, backup → game, game → (full) backup
  - Zeigt Pfade von Dateien ohne Gegenstück

### 1.2 Dateioperationslogik

#### Overwrite-Handling
Das Skript bietet differenzierte Optionen bei Dateikonflikt:
- **Overwrite**: Einzelne Datei überschreiben
- **Ignore**: Einzelne Datei überspringen
- **Overwrite all**: Alle Konflikte überschreiben
- **Ignore all**: Alle Konflikte überspringen
- **Ignore all webm**: Nur WEBM-Dateien überspringen
- **Cancel**: Operation abbrechen

#### Dateityp-Behandlung
- **Backup images**: PNG + WEBM
- **Extract/Move**: nur PNG
- **Return modified**: nur WEBP
- **Versioned Backup**: PNG + WEBM + WEBP
- **Count/Compare**: PNG + WEBP + WEBM

### 1.3 Pfadstruktur

```
Mind the School/
├── game/
│   └── images/          # Quellordner für Bilder
└── ../../../Image Extracter/
    ├── Mind the School Image Backup/       # Hauptbackup
    ├── Mind the School Full Image Backup/  # Vollbackup
    └── Mind the School Image Extract/      # Arbeitsordner
    
../../../Versioned Image Backups/
├── Version_0.1.0/
│   ├── lossy/
│   └── lossless/
├── Version_0.2.0/
│   ├── lossy/
│   └── lossless/
└── ...
```

### 1.4 Externe Abhängigkeiten

- **NConvert.exe**: Kommandozeilen-Tool für Bildkonvertierung
  - Pfad: `Image Converter/NConvert/nconvert.exe`
  - Parameter für lossless: `-overwrite -out webp -q -1 <file>`
  - Parameter für lossy: `-overwrite -out webp -q 90 <file>`

### 1.5 Identifizierte Schwachstellen

#### A. UI/UX-Probleme
1. **Primitive Dialoge**: pyautogui bietet nur einfache Messageboxen
2. **Keine Fortschrittsanzeige**: Benutzer sieht nicht, was gerade passiert
3. **Keine Vorschau**: Keine Möglichkeit, Dateien vor der Operation zu sehen
4. **Keine Undo-Funktion**: Operationen können nicht rückgängig gemacht werden
5. **Kein Drag & Drop**: Keine intuitive Dateiverwaltung
6. **Keine Dateivorschau**: Bilder können nicht angesehen werden
7. **Fehlendes Logging**: Keine persistente Historie der Operationen

#### B. Konfigurationsprobleme
1. **Hardcodierte Pfade**: Pfadstruktur ist fest im Code
2. **Keine Einstellungen**: Keine Möglichkeit, Standardwerte zu speichern
3. **Keine Profile**: Keine verschiedenen Konfigurationsprofile möglich
4. **Fehlende Validierung**: Pfadexistenz wird nicht vorab geprüft

#### C. Wartbarkeitsprobleme
1. **Monolithische Struktur**: Eine 343-zeilige main()-Funktion
2. **Code-Duplikation**: Pfadlogik wird mehrfach wiederholt
3. **Keine Trennung von Concerns**: UI, Logik und Dateioperationen vermischt
4. **Magic Strings**: Modusnamen als Strings statt Enums
5. **Fehlende Abstraktion**: Keine Interfaces für Operationen

#### D. Fehlerbehandlung
1. **Keine strukturierte Exception-Behandlung**: Crashes bei unerwarteten Fehlern
2. **Keine Transaktion**: Bei Fehler ist der Zustand inkonsistent
3. **Keine Validierung**: Dateigröße, Speicherplatz werden nicht geprüft
4. **Keine Retry-Logik**: Bei I/O-Fehlern wird nicht wiederholt

#### E. Erweiterbarkeit
1. **Fest an NConvert gebunden**: Keine anderen Konverter möglich
2. **Keine Plugin-Architektur**: Neue Operationen erfordern Core-Änderungen
3. **Keine Automatisierung**: Keine Möglichkeit für Batch-Jobs oder Scheduling
4. **Keine Scripting-API**: Keine programmatische Steuerung möglich

---

## 2. Zielarchitektur: C# WPF Anwendung

### 2.1 Architektur-Prinzipien

#### SOLID-Prinzipien
- **Single Responsibility**: Jede Klasse hat eine klar definierte Aufgabe
- **Open/Closed**: Erweiterbar ohne Änderung des Core-Codes
- **Liskov Substitution**: Operationen sind austauschbar
- **Interface Segregation**: Kleine, fokussierte Interfaces
- **Dependency Injection**: Loose Coupling durch DI

#### Architektur-Pattern
- **MVVM (Model-View-ViewModel)**: Trennung von UI und Logik
- **Repository Pattern**: Abstraktion der Datenzugriffe
- **Strategy Pattern**: Austauschbare Konvertierungs-/Operationsstrategien
- **Command Pattern**: Undo/Redo-Funktionalität
- **Observer Pattern**: Event-basierte Kommunikation

### 2.2 Projektstruktur

```
ImageBackupTool/
├── ImageBackupTool.sln
├── src/
│   ├── ImageBackupTool.Core/           # Kernlogik (Class Library)
│   │   ├── Models/
│   │   │   ├── FileItem.cs              # Repräsentiert eine Datei mit Metadaten
│   │   │   ├── OperationResult.cs       # Ergebnis einer Operation
│   │   │   ├── FileOperation.cs         # Basis für Dateioperationen
│   │   │   ├── BackupProfile.cs         # Backup-Konfiguration
│   │   │   └── OperationMode.cs         # Enum für Operationsmodi
│   │   ├── Interfaces/
│   │   │   ├── IFileOperation.cs        # Interface für Dateioperationen
│   │   │   ├── IImageConverter.cs       # Interface für Konverter
│   │   │   ├── IFileComparer.cs         # Interface für Vergleiche
│   │   │   ├── IPathResolver.cs         # Interface für Pfadauflösung
│   │   │   └── IOperationLogger.cs      # Interface für Logging
│   │   ├── Services/
│   │   │   ├── FileOperationService.cs  # Zentrale Dateioperationen
│   │   │   ├── BackupService.cs         # Backup-spezifische Logik
│   │   │   ├── PathResolverService.cs   # Pfadauflösung und -validierung
│   │   │   ├── OperationHistoryService.cs # Historie und Undo
│   │   │   └── ConfigurationService.cs  # Konfigurations-Management
│   │   ├── Operations/
│   │   │   ├── BackupOperation.cs       # Backup-Operation
│   │   │   ├── ExtractOperation.cs      # Extract-Operation
│   │   │   ├── ReturnOperation.cs       # Return-Operation
│   │   │   ├── ConvertOperation.cs      # Convert-Operation
│   │   │   ├── CompareOperation.cs      # Compare-Operation
│   │   │   └── CountOperation.cs        # Count-Operation
│   │   ├── Converters/
│   │   │   ├── NConvertImageConverter.cs # NConvert-Implementation
│   │   │   ├── ImageSharpConverter.cs    # Alternative: ImageSharp
│   │   │   └── ConverterFactory.cs       # Factory für Konverter
│   │   ├── Strategies/
│   │   │   ├── OverwriteStrategy.cs     # Strategie für Überschreiben
│   │   │   ├── ConflictResolution.cs    # Konfliktauflösung
│   │   │   └── FilterStrategy.cs        # Dateifilter-Strategien
│   │   └── Utilities/
│   │       ├── FileSystemHelper.cs      # Hilfsfunktionen für Dateisystem
│   │       ├── ImageMetadataReader.cs   # Auslesen von Bild-Metadaten
│   │       └── ValidationHelper.cs      # Validierungslogik
│   │
│   ├── ImageBackupTool.UI/             # WPF Anwendung
│   │   ├── ViewModels/
│   │   │   ├── MainViewModel.cs         # Hauptfenster ViewModel
│   │   │   ├── OperationViewModel.cs    # Operation-Auswahl ViewModel
│   │   │   ├── FileListViewModel.cs     # Dateilisten-ViewModel
│   │   │   ├── ProgressViewModel.cs     # Fortschrittsanzeige ViewModel
│   │   │   ├── SettingsViewModel.cs     # Einstellungen ViewModel
│   │   │   ├── HistoryViewModel.cs      # Historie ViewModel
│   │   │   └── CompareViewModel.cs      # Vergleichs-ViewModel
│   │   ├── Views/
│   │   │   ├── MainWindow.xaml          # Hauptfenster
│   │   │   ├── OperationSelectionView.xaml
│   │   │   ├── FileListView.xaml        # Dateiliste mit Preview
│   │   │   ├── ProgressView.xaml        # Fortschrittsanzeige
│   │   │   ├── SettingsWindow.xaml      # Einstellungsfenster
│   │   │   ├── HistoryWindow.xaml       # Historien-Fenster
│   │   │   └── CompareResultsView.xaml  # Vergleichsergebnisse
│   │   ├── Controls/
│   │   │   ├── ImagePreviewControl.xaml # Bildvorschau-Control
│   │   │   ├── FileTreeControl.xaml     # Dateibaum-Control
│   │   │   └── OperationCardControl.xaml # Operations-Karte
│   │   ├── Converters/                  # Value Converter für XAML
│   │   │   ├── BoolToVisibilityConverter.cs
│   │   │   ├── BytesToSizeConverter.cs
│   │   │   └── FileTypeToIconConverter.cs
│   │   ├── Behaviors/
│   │   │   ├── DragDropBehavior.cs      # Drag & Drop Verhalten
│   │   │   └── TreeViewSelectedItemBehavior.cs
│   │   ├── Commands/
│   │   │   ├── RelayCommand.cs          # Basis Command
│   │   │   └── AsyncRelayCommand.cs     # Async Command
│   │   └── Resources/
│   │       ├── Styles/
│   │       │   ├── ButtonStyles.xaml
│   │       │   ├── TextStyles.xaml
│   │       │   └── Colors.xaml
│   │       └── Icons/                   # Icon-Ressourcen
│   │
│   └── ImageBackupTool.Tests/          # Unit Tests
│       ├── Core/
│       │   ├── Operations/
│       │   └── Services/
│       └── UI/
│           └── ViewModels/
│
├── config/
│   └── appsettings.json                 # Standardkonfiguration
└── docs/
    ├── UserGuide.md                     # Benutzerhandbuch
    └── DeveloperGuide.md                # Entwicklerhandbuch
```

### 2.3 Kern-Komponenten Details

#### 2.3.1 Models

##### FileItem.cs
```csharp
public class FileItem : INotifyPropertyChanged
{
    public string FullPath { get; set; }
    public string RelativePath { get; set; }
    public string FileName { get; set; }
    public FileType Type { get; set; } // PNG, WEBP, WEBM
    public long Size { get; set; }
    public DateTime ModifiedDate { get; set; }
    public bool IsSelected { get; set; }
    public string Status { get; set; } // Pending, Processing, Completed, Error
    public BitmapImage Thumbnail { get; set; }
    public Dictionary<string, string> Metadata { get; set; }
}
```

##### OperationResult.cs
```csharp
public class OperationResult
{
    public bool Success { get; set; }
    public int ProcessedFiles { get; set; }
    public int SkippedFiles { get; set; }
    public int ErrorFiles { get; set; }
    public List<string> Errors { get; set; }
    public TimeSpan Duration { get; set; }
    public long TotalBytesProcessed { get; set; }
}
```

##### OperationMode.cs
```csharp
public enum OperationMode
{
    BackupImages,
    ExtractNewImages,
    CopyToExtract,
    ConvertImages,
    ReturnModifiedImages,
    CleanExtract,
    MoveBackupToExtract,
    MoveToVersionedBackup,
    ReturnFromVersionedBackup,
    ReturnVideos,
    Count,
    Compare
}

public enum ConversionQuality
{
    Lossless,
    Lossy
}

public enum FileConflictResolution
{
    Ask,
    Overwrite,
    Skip,
    OverwriteAll,
    SkipAll,
    SkipAllWebm
}
```

##### BackupProfile.cs
```csharp
public class BackupProfile
{
    public string Name { get; set; }
    public string SourcePath { get; set; }
    public string BackupPath { get; set; }
    public string FullBackupPath { get; set; }
    public string ExtractPath { get; set; }
    public string VersionedBackupPath { get; set; }
    public List<string> IncludeExtensions { get; set; }
    public List<string> ExcludeDirectories { get; set; }
    public FileConflictResolution DefaultConflictResolution { get; set; }
}
```

#### 2.3.2 Core Services

##### FileOperationService.cs
```csharp
public class FileOperationService : IFileOperationService
{
    private readonly IPathResolver _pathResolver;
    private readonly IOperationLogger _logger;
    
    // Kernfunktionen:
    // - CopyFileAsync() mit Progress-Reporting
    // - MoveFileAsync() mit Rollback-Fähigkeit
    // - DeleteFileAsync() mit Bestätigung
    // - ScanDirectoryAsync() mit Filter
    // - ValidateOperation() vor Ausführung
    // - ExecuteWithRetry() für I/O-Fehler
}
```

##### BackupService.cs
```csharp
public class BackupService : IBackupService
{
    private readonly IFileOperationService _fileOps;
    private readonly IOperationHistoryService _history;
    
    // Geschäftslogik für:
    // - CreateBackupAsync() - Vollständiges Backup
    // - IncrementalBackupAsync() - Nur geänderte Dateien
    // - RestoreBackupAsync() - Wiederherstellung
    // - CompareDirectoriesAsync() - Vergleich
    // - GenerateBackupReport() - Berichtserstellung
}
```

##### OperationHistoryService.cs
```csharp
public class OperationHistoryService : IOperationHistoryService
{
    // Funktionen:
    // - RecordOperation() - Speichert Operation
    // - GetHistory() - Lädt Historie
    // - UndoLastOperation() - Macht letzte Operation rückgängig
    // - CanUndo() - Prüft Undo-Möglichkeit
    // - ExportHistory() - Exportiert Historie (JSON/CSV)
}
```

#### 2.3.3 Operations

Jede Operation implementiert `IFileOperation`:

```csharp
public interface IFileOperation
{
    string Name { get; }
    string Description { get; }
    bool CanUndo { get; }
    
    Task<OperationResult> ExecuteAsync(
        IEnumerable<FileItem> files, 
        OperationParameters parameters,
        IProgress<OperationProgress> progress,
        CancellationToken cancellationToken);
        
    Task<bool> UndoAsync(CancellationToken cancellationToken);
    Task<bool> ValidateAsync(OperationParameters parameters);
}
```

Beispiel: **BackupOperation.cs**
```csharp
public class BackupOperation : IFileOperation
{
    // Spezifische Logik für Backup:
    // - Validierung der Zielpfade
    // - Prüfung von Speicherplatz
    // - Parallele Verarbeitung mit Semaphore
    // - Progress-Reporting
    // - Fehlersammlung und -behandlung
    // - Metadaten-Erhaltung
}
```

#### 2.3.4 Image Converter

```csharp
public interface IImageConverter
{
    Task<bool> ConvertAsync(
        string sourcePath, 
        string destinationPath, 
        ConversionParameters parameters,
        IProgress<double> progress,
        CancellationToken cancellationToken);
        
    bool SupportsFormat(string extension);
    List<string> SupportedFormats { get; }
}

public class NConvertImageConverter : IImageConverter
{
    // Wrapper für NConvert.exe:
    // - Process-Management
    // - Output-Parsing für Progress
    // - Error-Handling
    // - Timeout-Management
}

public class ImageSharpConverter : IImageConverter
{
    // Alternative mit ImageSharp Library:
    // - Native C# Implementation
    // - Keine externe Abhängigkeit
    // - Bessere Integration
}
```

---

## 3. UI/UX Design

### 3.1 Hauptfenster Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ Image Backup Tool                                    [_][□][X]  │
├─────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌──────────┐  │
│ │  Operations │ │   History   │ │  Settings   │ │   Help   │  │
│ └─────────────┘ └─────────────┘ └─────────────┘ └──────────┘  │
├─────────────────────────────────────────────────────────────────┤
│ Profile: [Mind the School ▼]                  [New] [Edit]      │
├─────────────────────────────────────────────────────────────────┤
│ ┌───────────────────────┬───────────────────────────────────┐   │
│ │ Operation Selection   │ Source: game/images               │   │
│ │                       │ ┌───────────────────────────────┐ │   │
│ │ ● Backup              │ │ □ characters/                 │ │   │
│ │ ○ Extract             │ │   ├─ □ alice/                 │ │   │
│ │ ○ Convert             │ │   │   ├─ ☑ alice_happy.png   │ │   │
│ │ ○ Return              │ │   │   ├─ ☑ alice_sad.png     │ │   │
│ │ ○ Versioned Backup    │ │   │   └─ ☑ alice_angry.png   │ │   │
│ │ ○ Compare             │ │   └─ □ bob/                   │ │   │
│ │ ○ Count               │ │ □ background/                 │ │   │
│ │                       │ │ □ events/                     │ │   │
│ │ [Advanced Options ▼]  │ │                               │ │   │
│ │                       │ └───────────────────────────────┘ │   │
│ │ Conflict Resolution:  │ 1,234 files | 567 MB              │   │
│ │ [Ask for each ▼]      │ [Select All] [Deselect All]       │   │
│ │                       │                                   │   │
│ │ [Execute Operation]   │ Preview:                          │   │
│ │                       │ ┌───────────────────────────────┐ │   │
│ │                       │ │                               │ │   │
│ │                       │ │   [Image Preview]             │ │   │
│ │                       │ │                               │ │   │
│ │                       │ │   alice_happy.png             │ │   │
│ │                       │ │   1920x1080 | 456 KB          │ │   │
│ │                       │ │   Modified: 2026-06-15        │ │   │
│ │                       │ └───────────────────────────────┘ │   │
│ └───────────────────────┴───────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│ Status: Ready │ Last backup: 2026-06-28 14:32 │ 2,456 files    │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Progress Dialog

```
┌─────────────────────────────────────────────┐
│ Backing up images...              [_][□][X] │
├─────────────────────────────────────────────┤
│                                             │
│ Overall Progress:                           │
│ ████████████████████░░░░░░░ 65% (650/1000)  │
│                                             │
│ Current File:                               │
│ characters/alice/alice_happy.png            │
│ ████████████████░░░░░░░░░░░ 55%             │
│                                             │
│ Speed: 12.5 MB/s                            │
│ Time remaining: ~30 seconds                 │
│ Processed: 325 MB / 500 MB                  │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ [LOG]                                   │ │
│ │ ✓ characters/alice/alice.png            │ │
│ │ ✓ characters/bob/bob.png                │ │
│ │ ⚠ characters/eve/eve.png (exists)       │ │
│ │ ✓ background/school.png                 │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│         [Pause]  [Cancel]  [Hide]           │
└─────────────────────────────────────────────┘
```

### 3.3 Settings Window

```
┌─────────────────────────────────────────────────────────────┐
│ Settings                                         [_][□][X]  │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────┬─────────────────────────────────────┐   │
│ │ General         │ Paths                               │   │
│ │ Paths           │                                     │   │
│ │ Operations      │ Source Directory (game/images):     │   │
│ │ Converter       │ [M:\...\game\images    ] [Browse]   │   │
│ │ Advanced        │                                     │   │
│ │                 │ Backup Directory:                   │   │
│ │                 │ [M:\...\Image Backup   ] [Browse]   │   │
│ │                 │                                     │   │
│ │                 │ Full Backup Directory:              │   │
│ │                 │ [M:\...\Full Backup    ] [Browse]   │   │
│ │                 │                                     │   │
│ │                 │ Extract Directory:                  │   │
│ │                 │ [M:\...\Image Extract  ] [Browse]   │   │
│ │                 │                                     │   │
│ │                 │ Versioned Backups Directory:        │   │
│ │                 │ [M:\...\Versioned Back] [Browse]    │   │
│ │                 │                                     │   │
│ │                 │ [✓] Validate paths on startup       │   │
│ │                 │ [✓] Create missing directories      │   │
│ │                 │                                     │   │
│ └─────────────────┴─────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                                    [Save]  [Cancel]  [Apply] │
└─────────────────────────────────────────────────────────────┘
```

### 3.4 UI-Features

#### 3.4.1 Drag & Drop
- Dateien/Ordner direkt auf die Anwendung ziehen
- Automatische Erkennung des Kontexts (Source/Destination)
- Visuelle Indikatoren für Drop-Zonen

#### 3.4.2 Image Preview
- Thumbnail-Ansicht in der Dateiliste
- Große Vorschau im Preview-Panel
- Metadaten-Anzeige (Größe, Auflösung, Datum)
- Zoom-Funktion
- Vergleichsansicht (Side-by-Side)

#### 3.4.3 Keyboard Shortcuts
- **Ctrl+B**: Backup starten
- **Ctrl+E**: Extract starten
- **Ctrl+R**: Return starten
- **Ctrl+H**: Historie anzeigen
- **Ctrl+S**: Einstellungen öffnen
- **Ctrl+Z**: Letzte Operation rückgängig
- **Space**: Datei-Auswahl togglen
- **Ctrl+A**: Alle auswählen

#### 3.4.4 Context Menu
Rechtsklick auf Dateien:
- Open in Explorer
- Open with default app
- Copy Path
- Show Metadata
- Compare with...
- Add to Favorites

#### 3.4.5 Themes
- Light Theme (Standard)
- Dark Theme
- High Contrast Theme
- Custom Theme Support

---

## 4. Konfiguration

### 4.1 appsettings.json

```json
{
  "AppSettings": {
    "Theme": "Light",
    "Language": "de-DE",
    "CheckForUpdates": true,
    "SaveWindowPosition": true
  },
  "Paths": {
    "SourcePath": "game/images",
    "BackupPath": "../../../Image Extracter/Mind the School Image Backup",
    "FullBackupPath": "../../../Image Extracter/Mind the School Full Image Backup",
    "ExtractPath": "../../../Image Extracter/Mind the School Image Extract",
    "VersionedBackupPath": "../../../Versioned Image Backups"
  },
  "Operations": {
    "DefaultConflictResolution": "Ask",
    "EnableParallelProcessing": true,
    "MaxParallelOperations": 4,
    "EnableLogging": true,
    "LogPath": "logs/",
    "RetainLogDays": 30,
    "ShowNotifications": true
  },
  "Converter": {
    "DefaultConverter": "NConvert",
    "NConvertPath": "NConvert/nconvert.exe",
    "LosslessQuality": -1,
    "LossyQuality": 90,
    "LossyDirectories": ["events", "background", "characters", "mods"],
    "AlwaysLosslessDirectories": ["ui", "gui"]
  },
  "Backup": {
    "AutoBackup": false,
    "AutoBackupInterval": 24,
    "MaxBackupVersions": 10,
    "CompressBackups": false,
    "VerifyAfterBackup": true
  },
  "FileTypes": {
    "SupportedImageFormats": [".png", ".webp", ".jpg", ".jpeg"],
    "SupportedVideoFormats": [".webm", ".mp4"],
    "DefaultOutputFormat": ".webp"
  }
}
```

### 4.2 Backup Profiles (JSON)

```json
{
  "Profiles": [
    {
      "Name": "Mind the School - Default",
      "IsDefault": true,
      "SourcePath": "M:\\MTS Project\\Mind the School\\game\\images",
      "BackupPath": "M:\\Image Extracter\\Mind the School Image Backup",
      "IncludeExtensions": [".png", ".webm"],
      "ExcludeDirectories": ["temp", "cache"],
      "ConflictResolution": "Ask"
    },
    {
      "Name": "Quick PNG Only",
      "IsDefault": false,
      "SourcePath": "M:\\MTS Project\\Mind the School\\game\\images",
      "BackupPath": "M:\\Quick Backup",
      "IncludeExtensions": [".png"],
      "ExcludeDirectories": [],
      "ConflictResolution": "OverwriteAll"
    }
  ]
}
```

### 4.3 User Preferences

Gespeichert in `%APPDATA%/ImageBackupTool/preferences.json`:
```json
{
  "WindowPosition": {
    "Left": 100,
    "Top": 100,
    "Width": 1200,
    "Height": 800,
    "Maximized": false
  },
  "RecentOperations": [
    {
      "Mode": "BackupImages",
      "Timestamp": "2026-06-28T14:32:00",
      "FilesProcessed": 1234
    }
  ],
  "Favorites": [
    "characters/alice/",
    "background/school/"
  ],
  "LastUsedProfile": "Mind the School - Default"
}
```

---

## 5. Erweiterte Features

### 5.1 Operation History & Undo

#### History-Datenstruktur
```json
{
  "OperationId": "guid",
  "Timestamp": "2026-06-28T14:32:00",
  "Mode": "BackupImages",
  "Profile": "Mind the School - Default",
  "FilesProcessed": 1234,
  "Success": true,
  "Duration": "00:02:34",
  "Changes": [
    {
      "Action": "Copy",
      "SourcePath": "game/images/alice.png",
      "DestinationPath": "backup/alice.png",
      "BackupPath": ".history/backup_guid/alice.png"
    }
  ]
}
```

#### Undo-Mechanismus
- Backup der überschriebenen Dateien in `.history/` Ordner
- Metadaten für Rollback (Original-Pfade, Timestamps)
- Undo-Stack mit maximaler Größe (konfigurierbar)
- Undo nur für letzte N Operationen möglich
- Automatische Cleanup alter History-Einträge

### 5.2 Batch Operations

```csharp
public class BatchOperationBuilder
{
    // Ermöglicht Verkettung von Operationen:
    var batch = new BatchOperationBuilder()
        .AddOperation(new BackupOperation())
        .AddOperation(new ConvertOperation())
        .AddOperation(new CleanOperation())
        .WithProfile("MTS-Default")
        .WithProgressCallback(OnProgress)
        .Build();
        
    await batch.ExecuteAsync();
}
```

**UI für Batch Operations:**
- Drag & Drop von Operationskarten
- Reihenfolge änderbar
- Bedingte Ausführung (nur wenn vorherige erfolgreich)
- Speichern von Batch-Vorlagen

### 5.3 Scheduling

```csharp
public class OperationScheduler
{
    // Geplante Ausführung von Operationen:
    // - Einmalig zu bestimmtem Zeitpunkt
    // - Wiederkehrend (täglich, wöchentlich)
    // - Bei bestimmten Events (Dateisystem-Änderung)
    // - Integration mit Windows Task Scheduler
}
```

**UI für Scheduling:**
- Kalender-View für geplante Operationen
- Quick-Presets (täglich um 2:00, wöchentlich Sonntag, etc.)
- Email-Benachrichtigung nach Ausführung

### 5.4 Vergleichsansicht (Compare)

#### Side-by-Side View
```
┌─────────────────────────────────────────────────────────────┐
│ Compare Results                                             │
├─────────────────────────────────────────────────────────────┤
│ Source: game/images                     ↔  Backup           │
│ ┌────────────────────────┬────────────────────────────────┐ │
│ │ Only in Source (12)    │ Only in Backup (3)             │ │
│ │ ├─ characters/new.png  │ ├─ characters/old.png          │ │
│ │ ├─ background/bg2.png  │ ├─ events/deleted.png          │ │
│ │ └─ ...                 │ └─ ...                         │ │
│ ├────────────────────────┼────────────────────────────────┤ │
│ │ Modified (45)          │ Identical (1,234)              │ │
│ │ ├─ alice.png           │ ├─ bob.png                     │ │
│ │ │  ├ Source: 456 KB    │ └─ ...                         │ │
│ │ │  └ Backup: 432 KB    │                                │ │
│ │ └─ ...                 │                                │ │
│ └────────────────────────┴────────────────────────────────┘ │
│                                                             │
│ [Export Report] [Sync Missing] [Show Differences]          │
└─────────────────────────────────────────────────────────────┘
```

#### Diff-Ansicht für Bilder
- Overlay-Modus mit Transparenz-Slider
- Side-by-Side Ansicht
- Difference-Map (Pixel-Differenzen hervorheben)
- Metadaten-Vergleich (Größe, Format, Kompression)

### 5.5 Advanced Filtering

```csharp
public class FileFilter
{
    // Filterkriterien:
    public List<string> IncludeExtensions { get; set; }
    public List<string> ExcludeExtensions { get; set; }
    public List<string> IncludeDirectories { get; set; }
    public List<string> ExcludeDirectories { get; set; }
    public long? MinSize { get; set; }
    public long? MaxSize { get; set; }
    public DateTime? ModifiedAfter { get; set; }
    public DateTime? ModifiedBefore { get; set; }
    public string NamePattern { get; set; } // Regex
    
    // Erweiterte Filter:
    public int? MinWidth { get; set; }
    public int? MinHeight { get; set; }
    public bool? HasAlpha { get; set; }
    public ImageFormat? Format { get; set; }
}
```

**UI für Filtering:**
- Filter-Builder mit Visual Editor
- Speichern von Filter-Presets
- Live-Vorschau der gefilterten Dateien

### 5.6 Report Generation

```csharp
public class ReportGenerator
{
    // Report-Typen:
    // - Operation Summary (Was wurde gemacht)
    // - File Inventory (Was ist wo)
    // - Comparison Report (Unterschiede)
    // - Space Usage Report (Speicherplatz-Analyse)
    // - Change History (Änderungen über Zeit)
    
    // Export-Formate:
    // - PDF
    // - HTML
    // - CSV
    // - JSON
}
```

### 5.7 Notifications

```csharp
public class NotificationService
{
    // Benachrichtigungstypen:
    // - Toast Notifications (Windows)
    // - Email (SMTP)
    // - Webhook (Slack, Discord, etc.)
    
    // Trigger:
    // - Operation abgeschlossen
    // - Operation fehlgeschlagen
    // - Speicherplatz kritisch
    // - Geplante Operation ausgeführt
}
```

---

## 6. Fehlerbehandlung & Validierung

### 6.1 Validierung vor Operation

```csharp
public class OperationValidator
{
    public ValidationResult Validate(IFileOperation operation, OperationParameters parameters)
    {
        var result = new ValidationResult();
        
        // Prüfungen:
        // 1. Pfad-Existenz
        result.Errors.AddRange(ValidatePaths(parameters));
        
        // 2. Schreibrechte
        result.Errors.AddRange(ValidatePermissions(parameters));
        
        // 3. Speicherplatz
        result.Errors.AddRange(ValidateDiskSpace(parameters));
        
        // 4. Datei-Locks
        result.Errors.AddRange(ValidateFileLocks(parameters));
        
        // 5. Zirkuläre Operationen
        result.Errors.AddRange(ValidateCircularOperations(parameters));
        
        return result;
    }
}
```

### 6.2 Exception Handling Strategy

```csharp
// Hierarchie von Custom Exceptions
public class ImageBackupException : Exception { }
public class PathNotFoundException : ImageBackupException { }
public class InsufficientSpaceException : ImageBackupException { }
public class FileAccessException : ImageBackupException { }
public class OperationCancelledException : ImageBackupException { }

// Global Exception Handler
public class GlobalExceptionHandler
{
    public void Handle(Exception ex, OperationContext context)
    {
        // Logging
        _logger.LogError(ex, "Operation failed", context);
        
        // User Notification
        if (ex is ImageBackupException knownEx)
        {
            ShowUserFriendlyError(knownEx);
        }
        else
        {
            ShowGenericError(ex);
            SendErrorReport(ex, context); // Telemetrie
        }
        
        // Rollback wenn möglich
        if (context.CanRollback)
        {
            RollbackOperation(context);
        }
    }
}
```

### 6.3 Retry Logic

```csharp
public class RetryPolicy
{
    // Konfigurierbare Retry-Strategie:
    public int MaxRetries { get; set; } = 3;
    public TimeSpan InitialDelay { get; set; } = TimeSpan.FromSeconds(1);
    public double BackoffMultiplier { get; set; } = 2.0;
    
    // Retry nur bei bestimmten Exceptions:
    public List<Type> RetriableExceptions { get; set; } = new()
    {
        typeof(IOException),
        typeof(UnauthorizedAccessException)
    };
    
    public async Task<T> ExecuteAsync<T>(Func<Task<T>> action)
    {
        // Exponential Backoff Implementation
    }
}
```

---

## 7. Testing Strategy

### 7.1 Unit Tests

```csharp
[TestFixture]
public class BackupOperationTests
{
    private Mock<IFileOperationService> _fileServiceMock;
    private BackupOperation _sut;
    
    [SetUp]
    public void Setup()
    {
        _fileServiceMock = new Mock<IFileOperationService>();
        _sut = new BackupOperation(_fileServiceMock.Object);
    }
    
    [Test]
    public async Task ExecuteAsync_ValidFiles_ShouldCopyAllFiles()
    {
        // Arrange
        var files = CreateTestFiles(10);
        var parameters = new OperationParameters();
        
        // Act
        var result = await _sut.ExecuteAsync(files, parameters, null, CancellationToken.None);
        
        // Assert
        Assert.That(result.Success, Is.True);
        Assert.That(result.ProcessedFiles, Is.EqualTo(10));
        _fileServiceMock.Verify(x => x.CopyFileAsync(It.IsAny<string>(), It.IsAny<string>(), It.IsAny<CancellationToken>()), Times.Exactly(10));
    }
    
    [Test]
    public async Task ExecuteAsync_InsufficientSpace_ShouldThrowException()
    {
        // Arrange
        var files = CreateLargeFiles();
        _fileServiceMock.Setup(x => x.GetAvailableSpace(It.IsAny<string>()))
            .Returns(1024); // 1 KB
        
        // Act & Assert
        Assert.ThrowsAsync<InsufficientSpaceException>(() => 
            _sut.ExecuteAsync(files, new OperationParameters(), null, CancellationToken.None));
    }
}
```

### 7.2 Integration Tests

```csharp
[TestFixture]
public class FileOperationServiceIntegrationTests
{
    private string _testDirectory;
    private FileOperationService _service;
    
    [SetUp]
    public void Setup()
    {
        _testDirectory = Path.Combine(Path.GetTempPath(), Guid.NewGuid().ToString());
        Directory.CreateDirectory(_testDirectory);
        _service = new FileOperationService(new PathResolverService());
    }
    
    [TearDown]
    public void TearDown()
    {
        Directory.Delete(_testDirectory, true);
    }
    
    [Test]
    public async Task CopyFileAsync_RealFile_ShouldCopySuccessfully()
    {
        // Test mit echtem Dateisystem
    }
}
```

### 7.3 UI Tests

```csharp
[TestFixture]
public class MainViewModelTests
{
    [Test]
    public void ExecuteBackupCommand_WhenCalled_ShouldUpdateProgress()
    {
        // Arrange
        var vm = new MainViewModel();
        bool progressChanged = false;
        vm.PropertyChanged += (s, e) => 
        {
            if (e.PropertyName == nameof(vm.Progress))
                progressChanged = true;
        };
        
        // Act
        vm.ExecuteBackupCommand.Execute(null);
        
        // Assert
        Assert.That(progressChanged, Is.True);
    }
}
```

### 7.4 Test Coverage Ziele

- **Core Library**: > 90% Code Coverage
- **Services**: > 85% Code Coverage
- **ViewModels**: > 80% Code Coverage
- **Operations**: > 95% Code Coverage (kritisch)

---

## 8. Performance-Optimierungen

### 8.1 Parallele Verarbeitung

```csharp
public class ParallelFileProcessor
{
    private readonly int _maxDegreeOfParallelism;
    private readonly SemaphoreSlim _semaphore;
    
    public ParallelFileProcessor(int maxParallel = 4)
    {
        _maxDegreeOfParallelism = maxParallel;
        _semaphore = new SemaphoreSlim(maxParallel);
    }
    
    public async Task ProcessFilesAsync(
        IEnumerable<FileItem> files,
        Func<FileItem, Task> processFunc,
        IProgress<double> progress)
    {
        var tasks = files.Select(async file =>
        {
            await _semaphore.WaitAsync();
            try
            {
                await processFunc(file);
            }
            finally
            {
                _semaphore.Release();
            }
        });
        
        await Task.WhenAll(tasks);
    }
}
```

### 8.2 Caching

```csharp
public class ThumbnailCache
{
    private readonly MemoryCache _cache;
    private readonly int _maxCacheSizeMB = 100;
    
    public BitmapImage GetOrCreate(string filePath, Func<string, BitmapImage> factory)
    {
        return _cache.GetOrCreate(filePath, entry =>
        {
            entry.Size = 1; // Schätzung
            entry.SlidingExpiration = TimeSpan.FromMinutes(10);
            return factory(filePath);
        });
    }
}
```

### 8.3 Lazy Loading

```csharp
public class LazyFileTree
{
    // Lädt Dateibaumstruktur nur bei Bedarf
    // Virtualisierung für große Dateilisten
    // Pagination für Tausende von Dateien
}
```

### 8.4 Buffered I/O

```csharp
public class BufferedFileCopier
{
    private const int BufferSize = 1024 * 1024; // 1 MB
    
    public async Task CopyAsync(string source, string dest, IProgress<long> progress)
    {
        using var sourceStream = new FileStream(source, FileMode.Open, FileAccess.Read, FileShare.Read, BufferSize, true);
        using var destStream = new FileStream(dest, FileMode.Create, FileAccess.Write, FileShare.None, BufferSize, true);
        
        await sourceStream.CopyToAsync(destStream, BufferSize, progress);
    }
}
```

---

## 9. Erweiterbarkeit

### 9.1 Plugin-Architektur

```csharp
public interface IPlugin
{
    string Name { get; }
    string Version { get; }
    string Description { get; }
    
    void Initialize(IServiceProvider services);
    void Shutdown();
}

public interface IOperationPlugin : IPlugin
{
    IFileOperation CreateOperation();
}

public interface IConverterPlugin : IPlugin
{
    IImageConverter CreateConverter();
}

public class PluginLoader
{
    private readonly string _pluginDirectory;
    
    public List<IPlugin> LoadPlugins()
    {
        // Lädt DLLs aus plugins/ Ordner
        // Reflection-basiertes Discovery
        // MEF (Managed Extensibility Framework) Integration
    }
}
```

### 9.2 Custom Operations

Entwickler können eigene Operationen hinzufügen:

```csharp
// In einem separaten Plugin-Projekt
public class ResizeOperation : IFileOperation
{
    public string Name => "Resize Images";
    public string Description => "Resizes images to specified dimensions";
    
    public async Task<OperationResult> ExecuteAsync(...)
    {
        // Custom Logik
    }
}
```

### 9.3 Scripting API

```csharp
public class ScriptingEngine
{
    private readonly ScriptEngine _engine;
    
    public void LoadScript(string scriptPath)
    {
        // C# Scripting API (Roslyn)
        // Erlaubt Benutzer-Scripts für Automatisierung
    }
    
    // Beispiel Script:
    // var tool = new ImageBackupTool();
    // tool.SetProfile("MTS-Default");
    // await tool.BackupAsync();
    // await tool.ConvertAsync(ConversionQuality.Lossy);
}
```

---

## 10. Sicherheit

### 10.1 Pfad-Validierung

```csharp
public class PathValidator
{
    public bool IsValidPath(string path)
    {
        // Prüfungen:
        // - Keine Path Traversal (.., ~)
        // - Keine verbotenen Zeichen
        // - Nicht System/Protected Folders
        // - Innerhalb erlaubter Roots
    }
}
```

### 10.2 Berechtigungen

```csharp
public class PermissionChecker
{
    public bool CanReadDirectory(string path)
    {
        // Prüft NTFS Permissions
    }
    
    public bool CanWriteDirectory(string path)
    {
        // Prüft Schreibrechte
    }
}
```

### 10.3 Sichere Datei-Operationen

```csharp
public class SecureFileOperations
{
    // Verhindert:
    // - Time-of-check to time-of-use (TOCTOU) Bugs
    // - Race Conditions
    // - Symlink Attacks
    
    public async Task SafeCopyAsync(string source, string dest)
    {
        // 1. Validierung
        // 2. Atomic operations wo möglich
        // 3. Exception-safe Cleanup
    }
}
```

---

## 11. Lokalisierung

### 11.1 Resource Files

```
Resources/
├── Strings.resx (Englisch - Standard)
├── Strings.de.resx (Deutsch)
└── Strings.fr.resx (Französisch)
```

### 11.2 Unterstützte Sprachen (Initial)

- Deutsch (de-DE)
- Englisch (en-US)

### 11.3 Dynamischer Sprachwechsel

```csharp
public class LocalizationService
{
    public void ChangeLanguage(CultureInfo culture)
    {
        Thread.CurrentThread.CurrentCulture = culture;
        Thread.CurrentThread.CurrentUICulture = culture;
        
        // Trigger UI Refresh
        OnLanguageChanged?.Invoke();
    }
}
```

---

## 12. Dokumentation

### 12.1 Inline-Dokumentation

```csharp
/// <summary>
/// Executes a backup operation on the specified files.
/// </summary>
/// <param name="files">The files to backup</param>
/// <param name="parameters">Operation parameters including destination path</param>
/// <param name="progress">Progress reporter for UI updates</param>
/// <param name="cancellationToken">Cancellation token for operation abort</param>
/// <returns>
/// An <see cref="OperationResult"/> containing statistics and errors.
/// </returns>
/// <exception cref="InsufficientSpaceException">
/// Thrown when destination drive has insufficient space
/// </exception>
public async Task<OperationResult> ExecuteAsync(...)
```

### 12.2 Benutzerhandbuch

Themen:
- Installation
- Erste Schritte
- Operation Guides (für jede Operation)
- Konfiguration
- Troubleshooting
- FAQ

### 12.3 Entwicklerhandbuch

Themen:
- Architektur-Übersicht
- Plugin-Entwicklung
- API-Referenz
- Best Practices
- Contribution Guidelines

---

## 13. Deployment

### 13.1 Installer

- **WiX Toolset** für MSI-Installer
- **ClickOnce** für Auto-Updates
- **MSIX Package** für Microsoft Store

### 13.2 Dependencies

```xml
<ItemGroup>
  <!-- WPF Framework -->
  <FrameworkReference Include="Microsoft.WindowsDesktop.App.WPF" />
  
  <!-- Dependency Injection -->
  <PackageReference Include="Microsoft.Extensions.DependencyInjection" />
  
  <!-- Configuration -->
  <PackageReference Include="Microsoft.Extensions.Configuration.Json" />
  
  <!-- Logging -->
  <PackageReference Include="Serilog" />
  <PackageReference Include="Serilog.Sinks.File" />
  
  <!-- UI Components -->
  <PackageReference Include="ModernWpfUI" />
  <PackageReference Include="MaterialDesignThemes" />
  
  <!-- Image Processing -->
  <PackageReference Include="SixLabors.ImageSharp" />
  
  <!-- Testing -->
  <PackageReference Include="NUnit" />
  <PackageReference Include="Moq" />
  <PackageReference Include="FluentAssertions" />
</ItemGroup>
```

### 13.3 Auto-Update

```csharp
public class UpdateService
{
    private readonly string _updateUrl = "https://example.com/updates";
    
    public async Task<bool> CheckForUpdatesAsync()
    {
        // Prüft auf neue Version
        // Zeigt Update-Dialog
        // Downloaded und installiert Update
    }
}
```

---

## 14. Verbesserungen gegenüber Python-Skript

### 14.1 Funktionale Verbesserungen

| Feature | Python-Skript | C# WPF App |
|---------|---------------|------------|
| **UI** | pyautogui Dialoge | Moderne WPF-Oberfläche |
| **Fortschritt** | Konsolen-Output | Echtzeit-Progress mit Details |
| **Vorschau** | Keine | Thumbnail + Full Preview |
| **Undo** | Keine | Vollständig mit History |
| **Konfiguration** | Hardcodiert | Datei + UI |
| **Fehlerbehandlung** | Minimal | Umfassend mit Rollback |
| **Logging** | Print-Statements | Strukturiertes Logging |
| **Parallelisierung** | Sequential | Parallel mit Semaphore |
| **Scheduling** | Keine | Windows Task Scheduler |
| **Benachrichtigungen** | pyautogui alerts | Toast + Email + Webhooks |
| **Vergleich** | Text-Output | Visual Diff + Reports |
| **Batch** | Keine | Verkettbare Operationen |
| **Plugins** | Keine | Vollständige Plugin-API |
| **Tests** | Keine | Unit + Integration Tests |
| **Updates** | Manuell | Auto-Update |
| **Lokalisierung** | Keine | Multi-Language |
| **Themes** | Keine | Light/Dark/Custom |
| **Drag & Drop** | Keine | Vollständig unterstützt |
| **Shortcuts** | Keine | Umfassende Tastenkürzel |

### 14.2 Technische Verbesserungen

- **Typsicherheit**: C# statt Python
- **Performance**: Native Code + Parallelisierung
- **Wartbarkeit**: SOLID-Architektur + Separation of Concerns
- **Testbarkeit**: Dependency Injection + Unit Tests
- **Erweiterbarkeit**: Plugin-System + Interfaces
- **Robustheit**: Exception Handling + Validation
- **Skalierbarkeit**: Async/Await + Streaming für große Dateien

### 14.3 UX-Verbesserungen

- **Intuitive Bedienung**: Drag & Drop, Context Menus
- **Sichtbarkeit**: Immer sichtbar was passiert
- **Kontrolle**: Pause, Cancel, Undo jederzeit möglich
- **Feedback**: Progress, Logs, Notifications
- **Flexibilität**: Profile, Filter, Batch-Operationen
- **Sicherheit**: Validierung, Bestätigungen, Rollback

---

## 15. Implementierungs-Roadmap

### Phase 1: Foundation (2-3 Wochen)
- ✅ Projektstruktur aufsetzen
- ✅ Core Models implementieren
- ✅ Basic FileOperationService
- ✅ Konfigurationssystem
- ✅ Grundlegendes Logging

### Phase 2: Core Operations (3-4 Wochen)
- ✅ BackupOperation
- ✅ ExtractOperation
- ✅ ReturnOperation
- ✅ ConvertOperation (NConvert Integration)
- ✅ CompareOperation
- ✅ CountOperation

### Phase 3: Basic UI (2-3 Wochen)
- ✅ MainWindow mit MVVM
- ✅ Operation Selection View
- ✅ File List View
- ✅ Basic Progress Dialog
- ✅ Settings Window

### Phase 4: Advanced Features (3-4 Wochen)
- ✅ Versioned Backup Operationen
- ✅ History & Undo System
- ✅ Image Preview
- ✅ Advanced Filtering
- ✅ Drag & Drop

### Phase 5: Polish & Enhancement (2-3 Wochen)
- ✅ Themes (Light/Dark)
- ✅ Lokalisierung (DE/EN)
- ✅ Keyboard Shortcuts
- ✅ Context Menus
- ✅ Notifications

### Phase 6: Testing & Documentation (2-3 Wochen)
- ✅ Unit Tests für Core
- ✅ Integration Tests
- ✅ UI Tests
- ✅ Benutzerhandbuch
- ✅ Entwicklerhandbuch

### Phase 7: Advanced Features 2 (2-3 Wochen)
- ✅ Plugin System
- ✅ Batch Operations
- ✅ Scheduling
- ✅ Report Generation
- ✅ Scripting API

### Phase 8: Release (1-2 Wochen)
- ✅ Installer
- ✅ Auto-Update
- ✅ Beta Testing
- ✅ Bug Fixes
- ✅ Release 1.0

**Geschätzte Gesamtdauer: 4-6 Monate**

---

## 16. Risiken & Mitigation

### 16.1 Technische Risiken

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|---------|------------|
| NConvert Integration | Mittel | Hoch | Alternative: ImageSharp |
| Performance bei vielen Dateien | Mittel | Mittel | Parallelisierung + Virtualisierung |
| WPF Komplexität | Niedrig | Mittel | Moderne UI Frameworks (ModernWPF) |
| Datenverlust durch Bugs | Niedrig | Sehr Hoch | Umfangreiche Tests + Undo System |

### 16.2 Projektrisiken

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|---------|------------|
| Scope Creep | Hoch | Mittel | Strikte Priorisierung nach Phasen |
| Zeitüberschreitung | Mittel | Mittel | MVP-Ansatz, optionale Features später |
| Komplexität unterschätzt | Mittel | Hoch | Regelmäßige Reviews, frühes Prototyping |

---

## 17. Success Metrics

### 17.1 Funktionale Metriken
- ✅ 100% Feature-Parität mit Python-Skript
- ✅ < 5% Fehlerrate bei Operationen
- ✅ 0 Datenverlust-Incidents

### 17.2 Performance-Metriken
- ✅ 2x schneller als Python-Skript (durch Parallelisierung)
- ✅ < 2 Sekunden Startzeit
- ✅ < 100 MB Memory-Verbrauch (idle)

### 17.3 UX-Metriken
- ✅ < 30 Sekunden für neue Benutzer um erste Operation durchzuführen
- ✅ < 3 Klicks für häufigste Operationen
- ✅ 95% positive User Feedback

### 17.4 Wartbarkeits-Metriken
- ✅ > 80% Code Coverage
- ✅ 0 Critical Security Issues
- ✅ < 1 Tag für neue Operation-Implementation

---

## 18. Zusammenfassung

### Kernziele
1. **Funktionalität**: Vollständige Migration aller Features des Python-Skripts
2. **Verbesserung**: Moderne UI, bessere UX, mehr Features
3. **Wartbarkeit**: Saubere Architektur, Tests, Dokumentation
4. **Erweiterbarkeit**: Plugin-System, Scripting, Batch-Operations

### Hauptvorteile der neuen Anwendung
- 🎨 **Moderne Benutzeroberfläche** statt primitive Dialoge
- ⚡ **Bessere Performance** durch Parallelisierung
- 🔄 **Undo/Redo** für sichere Operationen
- 📊 **Detaillierte Progress & Logging**
- 🔌 **Erweiterbar** durch Plugins
- 🧪 **Getestet** mit umfassender Test-Suite
- 🌍 **Mehrsprachig** (DE/EN)
- 🎨 **Themes** (Light/Dark)
- 📅 **Scheduling** für Automatisierung
- 📧 **Benachrichtigungen** (Toast/Email/Webhook)

### Nächste Schritte
1. Review und Freigabe dieses Plans
2. Setup der Entwicklungsumgebung
3. Start mit Phase 1 (Foundation)
4. Iterative Entwicklung nach Roadmap
5. Kontinuierliches Testing und Feedback

---

**Ende des Migration Plans**
