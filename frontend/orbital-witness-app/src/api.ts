import config from './config';

export interface UsageData {
    message_id: number;
    timestamp: string;
    report_name: string | null;
    credits_used: number;
  }
  
  export const fetchUsageData = async (): Promise<UsageData[]> => {
    const response = await fetch(config.API_BASE_URL);
    const data = await response.json();
    return data.usage;
  };
  