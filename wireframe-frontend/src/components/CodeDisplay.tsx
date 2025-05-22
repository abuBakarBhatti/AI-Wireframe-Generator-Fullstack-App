import { Box, Paper, Button, Tooltip } from '@mui/material';
import { useState } from 'react';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import DoneIcon from '@mui/icons-material/Done';

interface CodeDisplayProps {
  code: string;
  language: string;
}

const CodeDisplay = ({ code, language }: CodeDisplayProps) => {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Box sx={{ position: 'relative' }}>
      <Paper 
        component="pre"
        sx={{
          p: 3,
          overflowX: 'auto',
          fontFamily: '"Fira Code", "Roboto Mono", monospace',
          fontSize: '0.875rem',
          backgroundColor: '#282c34',
          color: '#abb2bf',
          borderRadius: 2,
          maxHeight: '500px',
          overflow: 'auto',
        }}
      >
        <Box sx={{ position: 'absolute', top: 8, right: 8 }}>
          <Tooltip title={copied ? "Copied!" : "Copy to clipboard"}>
            <Button
              onClick={copyToClipboard}
              size="small"
              variant="contained"
              color={copied ? "success" : "secondary"}
              sx={{ 
                minWidth: '40px',
                height: '40px',
                borderRadius: '50%',
              }}
            >
              {copied ? <DoneIcon fontSize="small" /> : <ContentCopyIcon fontSize="small" />}
            </Button>
          </Tooltip>
        </Box>
        <code className={`language-${language}`} style={{ whiteSpace: 'pre-wrap' }}>
          {code}
        </code>
      </Paper>
    </Box>
  );
};

export default CodeDisplay;






// const CodeDisplay = ({ code, language }: CodeDisplayProps) => {
//   return (
//     <Box sx={{ position: 'relative' }}>
//       <Paper 
//         component="pre"
//         sx={{
//           p: 2,
//           overflowX: 'auto',
//           fontFamily: 'monospace',
//           fontSize: '0.875rem',
//           backgroundColor: '#f5f5f5',
//           borderRadius: 1,
//           maxHeight: '400px',
//           overflow: 'auto',
//         }}
//       >
//         <code className={`language-${language}`}>
//           {code}
//         </code>
//       </Paper>
//     </Box>
//   );
// };

// export default CodeDisplay;