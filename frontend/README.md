# AI Stock Analytics Frontend

This project is the frontend for the AI Stock Analytics application, built using Vite, React, TypeScript, Tailwind CSS, Recharts, and Axios. It provides a user-friendly interface for analyzing stock data and visualizing trends.

## Features

- **Stock Input**: Users can enter stock symbols to fetch data.
- **Stock Charts**: Visual representation of stock trends using Recharts.
- **Chat Interface**: Interactive component for querying stock data.
- **Analysis Results**: Displays summaries and detailed analysis of stock performance.

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```
   or
   ```
   yarn install
   ```

### Running the Application

To start the development server, run:
```
npm run dev
```
or
```
yarn dev
```

Open your browser and navigate to `http://localhost:3000` to view the application.

### Building for Production

To create a production build, run:
```
npm run build
```
or
```
yarn build
```

The build artifacts will be stored in the `dist` directory.

## Folder Structure

- `src/`: Contains all source code files.
  - `components/`: Reusable React components.
  - `services/`: API service for making HTTP requests.
  - `hooks/`: Custom hooks for managing state and side effects.
  - `styles/`: Global styles and Tailwind CSS configuration.
- `public/`: Static assets.
- `index.html`: Main HTML file for the application.
- `package.json`: Project metadata and dependencies.
- `vite.config.ts`: Vite configuration file.

## License

This project is licensed under the MIT License. See the LICENSE file for details.