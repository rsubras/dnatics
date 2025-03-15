import React, { useEffect, useState, useMemo } from 'react';
import { PowerBIEmbed } from 'powerbi-client-react';
import { models } from 'powerbi-client';

import { Box} from '@mui/material';
import { PUBLIC_CLIENT_APPLICATION, TOKEN_REQUEST } from '../msalConfig';
import html2canvas from 'html2canvas';


const LeftContainer = () => {
  const [isClient, setIsClient] = useState(false);
  const [embedConfig,setEmbedConfig] = useState(null);
  const [narrative, setNarrative] = useState('');

  
  const reportId = "96eb11ea-82af-4bde-9fca-1ada030a84a1";
  const groupId = "37e6279c-d190-4d2b-b1ba-f96be8af1993";
  useEffect(() => {
    setIsClient(true);
  

  const acquireToken = async () => {
    try {
    const tokenResponse = await PUBLIC_CLIENT_APPLICATION.acquireTokenSilent(TOKEN_REQUEST);
    const accessToken = tokenResponse.accessToken;
  
  const EMBED_URL = `https://app.powerbi.com/reportEmbed?reportId=${reportId}`;
      console.log("Embed URL: ", EMBED_URL);
      console.log("Access Token: ", accessToken);
  setEmbedConfig({
    type: 'report',
    id: reportId,
    embedUrl: EMBED_URL,
    accessToken: accessToken,
    tokenType: models.TokenType.Aad,
    settings: {
      panes: {
        filters: {
          expanded: false,
          visible: false
        }
      },
    }
  });
} catch (error) {
  console.error("Error acquiring token:", error);
}
};

acquireToken();
  }, [reportId, groupId]);
  const captureReportAsImage = async () => {
    const reportElement = document.querySelector('.Embed-container');
    if (reportElement) {
      const canvas = await html2canvas(reportElement);
      const imgData = canvas.toDataURL('image/png');
      const link = document.createElement('a');
      link.href = imgData;
      link.download = 'report.png';
      link.click();
    }
  };
  const generateNarrative = async () => {
    if (window.report) {
      let pages = await window.report.getPages();

// Retrieve the first page.
    let firstPage = pages[0];
    let visual = await firstPage.getVisuals();
    const imageVisuals = visual.filter(visual => visual.type === "shape");
    console.log("Visuals:",visual);
    console.log("Image Visuals:",imageVisuals);
    return;
console.log(visuals);
      const visuals = await window.report.getVisuals();
      const visualData = visuals.map(visual => visual.title);
      
      const response = await fetch('https://api.openai.com/v1/engines/davinci-codex/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer YOUR_OPENAI_API_KEY`
        },
        body: JSON.stringify({
          prompt: `Generate a narrative based on the following visual data: ${visualData.join(', ')}`,
          max_tokens: 150
        })
      });

      const data = await response.json();
      setNarrative(data.choices[0].text);
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
        backgroundColor: '#f5f5f5',
      }}
    >
      {isClient && embedConfig && <PowerBIEmbed
          embedConfig={embedConfig}

          eventHandlers={
            new Map([
              ['loaded', function () { console.log('Report loaded'); }],
              ['rendered', function () { console.log('Report rendered'); }],
              ['error', function (event) { console.log("Error occured:",event.detail); }]
            ])
          }

          cssClassName={"Embed-container"}

          getEmbeddedComponent={(embeddedReport) => {
            window.report = embeddedReport;
          }}
        />}
     
    </Box>
  );
};

export default LeftContainer;