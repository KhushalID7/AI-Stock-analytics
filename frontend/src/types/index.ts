// This file defines shared TypeScript types for the application, including API response types.

export interface StockPrice {
    symbol: string;
    date: string;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
}

export interface StockAnalysisResult {
    symbol: string;
    movingAverages: {
        [window: number]: number[];
    };
    bollingerBands: {
        upper: number[];
        lower: number[];
        middle: number[];
    };
    lastValues: {
        price: number;
        movingAverage: number;
        upperBand: number;
        lowerBand: number;
    };
}

export interface AgentResponse {
    summary: string;
    raw_result: any;
    chart_urls: string[];
}

export interface ApiResponse<T> {
    data: T;
    message?: string;
    error?: boolean;
}

// Legacy type for compatibility
export type StockData = StockAnalysisResult;