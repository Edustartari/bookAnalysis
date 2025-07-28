import React, { useState, useEffect } from 'react';
import '/css/App.css';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import CircularProgress from '@mui/material/CircularProgress';


export default function AppMobile() {
	function check_local_storage() {
		let book_searches = localStorage.getItem('book_searches');
		if (book_searches === null) {
			book_searches = {};
		} else {
			book_searches = JSON.parse(book_searches);
		}
		return book_searches;
	}

	const [tab, setTab] = React.useState(0);
	const [currentBook, setCurrentBook] = React.useState({});
	const [search, setSearch] = React.useState('');
	const [loadingFetch, setLoadingFetch] = React.useState(false);
	const [loadingAnalysis, setLoadingAnalysis] = React.useState(false);
	const [analysisText, setAnalysisText] = React.useState('Pick an analysis...');
	const [latestSearches, setLatestSearches] = React.useState({});

	const changeTab = (event, newValue) => {
		setTab(newValue);
	};

	useEffect(() => {
		setLatestSearches(check_local_storage());
	}, []);

	async function search_book(value) {
		if(value === '') return;

		setTab(0);
		setAnalysisText('Pick an analysis...');
		setLoadingFetch(true);

		setSearch('');

		// Check if value is a number
		let book_id = parseInt(value);
		if (isNaN(book_id)) {
			alert('Please enter a valid book ID (number).');
			setLoadingFetch(false);
			return;
		}

		// Check if book_id already exists in local storage
		let book_searches = check_local_storage();
		if (book_id in book_searches) {
			let current_book = book_searches[book_id];
			setCurrentBook(current_book);
			setLoadingFetch(false);
			return;
		}
		
		// Fetch book data
		let result = false
		try {
			const response = await fetch(`/search/${book_id}`);
			let text = await response.text();
			let json_data = JSON.parse(text);
			if (response.status !== 200) {
				alert(json_data?.message || 'Error fetching book data. Please try again later.');
				setLoadingFetch(false);
				return;
			}
			if( json_data.status_message === 'error') {
				alert(json_data.message || 'Error fetching book data. Please try again later.');
				setLoadingFetch(false);
				return;
			}
			result = json_data.data
			setCurrentBook(result);

			// Save search to local storage
			book_searches[book_id] = result;
			localStorage.setItem('book_searches', JSON.stringify(book_searches));
			
			// And update latest searches
			let currentLatest = latestSearches;
			currentLatest[book_id] = result;
			setLatestSearches(currentLatest);
		} catch (error) {
			alert('Error fetching book data. Please try again later.');
		} finally {
			setLoadingFetch(false);
		}
	}

	async function analysis(action) {
		setLoadingAnalysis(true);

		if(action in currentBook['analysis']) {
			setAnalysisText(currentBook['analysis'][action]);
			setLoadingAnalysis(false);
			return;
		}
		
		// Fetch book data
		const response = await fetch(`/analysis/?book_id=${currentBook['book_id']}&action=${action}`);
		let text = await response.text();
		let json = JSON.parse(text);
		setAnalysisText(json.data);

		// Update current book with the new analysis
		let book = Object.assign({}, currentBook);
		book['analysis'][action] = json.data;
		setCurrentBook(book);
		
		setLoadingAnalysis(false);
		
		// Save new_analysis to local storage
		let book_searches = check_local_storage();
		book_searches[currentBook['book_id']]['analysis'][action] = json.data;
		localStorage.setItem('book_searches', JSON.stringify(book_searches));
	}

	return (
		<div className='app-main-background'>
			<div className='app-search-container'>
				<TextField value={search} onChange={(e) => setSearch(e.target.value)} className='app-search-textfield' id="outlined-basic" label="BOOK ID" variant="outlined" />
				<Button onClick={() => search_book(search)} disabled={loadingFetch || loadingAnalysis} className='app-search-button' variant="contained">SEARCH</Button>
			</div>
			{JSON.stringify(currentBook) === '{}' && loadingFetch && 
				<div className='app-main-loading' style={{margin: 20}}>Loading...</div>
			}
			{JSON.stringify(currentBook) !== '{}' &&
				<div className='app-main-container'>
					<div className='app-tabs-container'>
						<Tabs value={tab} onChange={changeTab} aria-label="basic tabs example" className='app-tabs'>
							<Tab label="INFO" index={0} disabled={loadingFetch || loadingAnalysis} />
							<Tab label="ANALYSIS" index={1} disabled={loadingFetch || loadingAnalysis} />
						</Tabs>
					</div>
					{loadingFetch &&
						<div className='app-loading'><CircularProgress /></div>
					}
					{!loadingFetch &&
						<>
							{tab === 0 &&
								<div className='app-main-info'>
									<div className='app-main-info-details'>
										<div className='app-main-info-details-title'>{currentBook.title}</div>
										<div className='app-main-info-details-author'>{currentBook.author}</div>
										<div className='app-main-info-details-description'>
											<div className='app-main-info-details-description-text'>Language:  {currentBook.language}</div>
											<div className='app-main-info-details-description-text'>Release Date:  {currentBook.release_date}</div>
											<div className='app-main-info-details-description-text'>Note:  {currentBook.note}</div>
											<div className='app-main-info-details-description-text'>Credits:  {currentBook.credits}</div>
										</div>
									</div>
									<div className='app-main-info-buttons'>
										{currentBook.read_online &&
											<Button variant="outlined" disabled={loadingFetch || loadingAnalysis} onClick={() => window.open(currentBook.read_online, '_blank')}>READ ONLINE</Button>
										}
										<Button variant="outlined" disabled={loadingFetch || loadingAnalysis} onClick={() => window.open(currentBook.download_html)}>DOWNLOAD HTML</Button>
									</div>
								</div>
							}
							{tab === 1 &&
								<div className='app-analysis'>
									<div className='app-analysis-buttons'>
										<Button variant="outlined" disabled={loadingFetch || loadingAnalysis} onClick={() => analysis('characters')}>Key Characters</Button>
										<Button variant="outlined" disabled={loadingFetch || loadingAnalysis} onClick={() => analysis('language')}>Language Detection</Button>
										<Button variant="outlined" disabled={loadingFetch || loadingAnalysis} onClick={() => analysis('sentiment')}>Sentiment Analysis</Button>
										<Button variant="outlined" disabled={loadingFetch || loadingAnalysis} onClick={() => analysis('summary')}>Plot Summary</Button>
									</div>
									{loadingAnalysis &&
										<div className='app-loading' style={{marginBottom: 25}}><CircularProgress /></div>
									}
									{!loadingAnalysis &&
										<div className='app-analysis-text'>{analysisText}</div>
									}
								</div>
							}
						</>
					}
				</div>
			}
			<div className='app-latest-container'>
				<div className='app-latest-title'>Latest Searches</div>
				{Object.keys(latestSearches).length === 0 &&
					<div className='app-latest-no-searches'>No searches yet</div>
				}
				{Object.keys(latestSearches).length > 0 &&
					<div className='app-latest-table'>
						<div className='app-latest-table-row'>
							<div className='app-latest-table-column-id app-latest-table-column-header'>ID</div>
							<div className='app-latest-table-column app-latest-table-column-header'>Title</div>
						</div>
						{Object.keys(latestSearches).map((id) => {
							return (
								<div key={id} className='app-latest-table-row'>
									<div className='app-latest-table-column-id'>
										<span onClick={() => search_book(id)}>{id}</span>
									</div>
									<div className='app-latest-table-column'>{latestSearches[id].title}</div>
								</div>
							);
						})}					
					</div>
				}
			</div>
		</div>
	);
}
