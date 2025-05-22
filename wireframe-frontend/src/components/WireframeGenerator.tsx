import { Alert, Backdrop, Box, Button, Card, CircularProgress, Divider, Fade, Grid, Paper, Tab, Tabs, TextField, Typography } from '@mui/material'
import React, { useState } from 'react'
import { generateWireframe } from '../api/wireframeApi'
import type { WireframeResponse } from '../types/types'
import SvgRenderer from './SvgRenderer'
import CodeDisplay from './CodeDisplay'
import PreviewIcon from '@mui/icons-material/Preview';
import CodeIcon from '@mui/icons-material/Code';
import SendIcon from '@mui/icons-material/Send';
import ListAltIcon from '@mui/icons-material/ListAlt';
import SchemaIcon from '@mui/icons-material/Schema';



const WireframeGenerator = () => {

    const [query, setQuery] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string |null>(null)
    const [response, setResponse] = useState<WireframeResponse | null>(null)
    const [tabValue, setTabValue] = useState(0)
    const [progress, setProgress] = useState(0);




    const handleQueryChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setQuery(e.target.value)
    }

    // Simulated progress for the loading indicator
    const simulateProgress = () => {
        setProgress(0);
        const interval = setInterval(() => {
        setProgress((prevProgress) => {
            // Don't reach 100% as that would indicate completion
            // We'll set it to 100 when the actual response arrives
            const newProgress = prevProgress + (Math.random() * 10);
            return newProgress >= 95 ? 95 : newProgress;
        });
        }, 500);
        
        return interval;
    };


    const handleSubmit = async () => {
        if (!query.trim()){
            setError('Please enter a valid query');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const result = await generateWireframe(query)
            console.log(result)

            if (result.errors && result.errors.length > 0) {
                setError(result.errors.join(', '));
                
            } else {
                setResponse(result);
            }
        } catch (err) {
            setError((err as Error).message);
        } finally {
            clearInterval(simulateProgress());
            setLoading(false);
            setProgress(100);
            // Small delay to show 100% complete before hiding the loader
            setTimeout(() => {
                setLoading(false);
            },  500);
        }
    }

    const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
        setTabValue(newValue);
    };

    return (
        <Box sx={{ maxWidth: 1200, mx: 'auto', p: 3 }}>
          <Paper 
            elevation={0} 
            sx={{ 
              p: 3, 
              mb: 4, 
              backgroundImage: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              borderRadius: 2
            }}
          >
            <Typography variant="h4" gutterBottom fontWeight="bold">
              Wireframe Generator
            </Typography>
            <Typography variant="body1">
              Describe your UI needs and let AI generate a wireframe for you
            </Typography>
          </Paper>
          
          <Paper sx={{ p: 3, mb: 4, borderRadius: 2 }}>
            <TextField
              fullWidth
              label="Describe your wireframe"
              variant="outlined"
              value={query}
              onChange={handleQueryChange}
              disabled={loading}
              multiline
              rows={3}
              placeholder="E.g. Create a responsive landing page for a fitness app with a hero section, features, and contact form"
              sx={{ mb: 2 }}
            />
            
            <Button 
              variant="contained" 
              color="primary" 
              onClick={handleSubmit}
              disabled={loading}
              endIcon={<SendIcon />}
              size="large"
              sx={{ 
                px: 4, 
                py: 1, 
                borderRadius: 2,
                background: 'linear-gradient(90deg, #6366F1 0%, #8B5CF6 100%)',
                '&:hover': {
                  background: 'linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%)',
                }
              }}
            >
              Generate Wireframe
            </Button>
          </Paper>
    
          {error && (
            <Alert 
              severity="error" 
              sx={{ mb: 4, borderRadius: 2 }}
              variant="filled"
            >
              {error}
            </Alert>
          )}
    
          {/* Loading backdrop with progress */}
          <Backdrop
            sx={{ 
              color: '#fff', 
              zIndex: (theme) => theme.zIndex.drawer + 1,
              flexDirection: 'column'
            }}
            open={loading}
          >
            <CircularProgress 
              color="inherit" 
              variant="determinate" 
              value={progress} 
              size={60}
              thickness={4}
              sx={{ mb: 2 }}
            />
            <Paper sx={{ 
              p: 3, 
              backgroundColor: 'rgba(255, 255, 255, 0.9)', 
              borderRadius: 2,
              maxWidth: 300,
              textAlign: 'center'
            }}>
              <Typography variant="h6" color="primary">
                Generating Wireframe
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {progress < 30 && "Analyzing your requirements..."}
                {progress >= 30 && progress < 60 && "Planning wireframe structure..."}
                {progress >= 60 && progress < 90 && "Creating SVG wireframe..."}
                {progress >= 90 && "Finalizing..."}
              </Typography>
            </Paper>
          </Backdrop>
    
          <Fade in={response !== null}>
            <Box>
              {response && (
                <Card sx={{ borderRadius: 2, overflow: 'hidden' }}>
                  <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                    <Tabs 
                      value={tabValue} 
                      onChange={handleTabChange}
                      variant="scrollable"
                      scrollButtons="auto"
                      sx={{
                        '& .MuiTab-root': {
                          minHeight: '64px',
                        }
                      }}
                    >
                      <Tab icon={<PreviewIcon />} label="Wireframe Preview" iconPosition="start" />
                      <Tab icon={<CodeIcon />} label="SVG Code" iconPosition="start" />
                      {response.detailed_requirements && (
                        <Tab icon={<ListAltIcon />} label="Requirements" iconPosition="start" />
                      )}
                      {response.wireframe_plan && (
                        <Tab icon={<SchemaIcon />} label="Wireframe Plan" iconPosition="start" />
                      )}
                    </Tabs>
                  </Box>
    
                  <Box sx={{ p: 3 }}>
                    {tabValue === 0 && (
                      <SvgRenderer svgCode={response.svg_code} />
                    )}
                    
                    {tabValue === 1 && (
                      <CodeDisplay code={response.svg_code} language="xml" />
                    )}
                  </Box>
                </Card>
              )}
            </Box>
          </Fade>
        </Box>
      );
    };
    
    export default WireframeGenerator;